#!/usr/bin/env python3
"""Fatia um STL/3MF para a Anycubic Kobra 3 Max e grava o G-code no formato
do Anycubic Slicer Next (cabecalho, miniatura, blocos executavel/config).

Uso:
  slice_k3max.py MODELO.stl --filament PETG [--out arquivo.gcode]
                 [--infill 20] [--walls 3] [--supports auto|on|off]
                 [--brim 5] [--layer 0.2] [--nozzle-temp T] [--bed-temp T]
                 [--orient auto|none|x90|x-90|y90|y-90|x180]
"""
import argparse, base64, datetime, io, json, os, re, shutil, struct, subprocess, sys, tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILES = os.path.join(HERE, '..', 'profiles')
BED_X, BED_Y, MAX_Z = 426, 420, 500
APP = 'AnycubicSlicerNext 2.0.0.6'
# linhas de config que o firmware da Kobra 3 Max nao consegue ler
BAD_PREFIXES = ('; filament_adaptive_volumetric_speed', '; filament_adhesiveness_category',
                '; filament_change_length', '; filament_colour_type',
                '; bed_temperature_formula = by_first_filament')


# ---------------------------------------------------------------- malha
def load_mesh(path):
    if path.lower().endswith('.3mf'):
        import zipfile, xml.etree.ElementTree as ET
        z = zipfile.ZipFile(path)
        name = next(n for n in z.namelist() if n.lower().endswith('.model'))
        root = ET.fromstring(z.read(name))
        tris = []
        for mesh in root.iter():
            if not mesh.tag.endswith('mesh'):
                continue
            vs = np.array([[float(v.get(a)) for a in 'xyz'] for v in mesh.iter() if v.tag.endswith('vertex')])
            ts = np.array([[int(t.get(a)) for a in ('v1', 'v2', 'v3')] for t in mesh.iter() if t.tag.endswith('triangle')])
            if len(ts):
                tris.append(vs[ts])
        return np.concatenate(tris)
    data = open(path, 'rb').read()
    n = struct.unpack('<I', data[80:84])[0] if len(data) >= 84 else 0
    if len(data) == 84 + 50 * n:
        rec = np.frombuffer(data[84:], dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]))
        return rec['v'].reshape(-1, 3, 3).astype(np.float64)
    vs = [float(x) for x in re.findall(rb'vertex\s+(\S+)\s+(\S+)\s+(\S+)', data) for x in x]
    return np.array(vs).reshape(-1, 3, 3)


ROTATIONS = {
    'none': np.eye(3),
    'x90': np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
    'x-90': np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),
    'y90': np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
    'y-90': np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
    'x180': np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]),
}


def contact_and_overhang(T):
    """Area apoiada na mesa e area pendente (precisa de suporte) com Z para cima."""
    N = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    A = np.linalg.norm(N, axis=1) / 2
    nz = N[:, 2] / (2 * A + 1e-12)
    zmin = T[:, :, 2].min()
    zc = T[:, :, 2].mean(1)
    down = nz < -0.707  # face virada para baixo mais de 45 graus
    on_bed = down & (T[:, :, 2].max(1) - zmin < 0.05)
    hanging = down & (zc - zmin > 0.3)
    return A[on_bed].sum(), A[hanging].sum()


def orient(T, mode):
    if mode != 'auto':
        return T @ ROTATIONS[mode].T, mode
    best = None
    for name, R in ROTATIONS.items():
        U = T @ R.T
        h = np.ptp(U[:, :, 2])
        if np.ptp(U[:, :, 0]) > BED_X or np.ptp(U[:, :, 1]) > BED_Y or h > MAX_Z:
            continue
        contact, hang = contact_and_overhang(U)
        score = contact / max(h, 1) ** 0.5 - 0.02 * hang
        if best is None or score > best[0]:
            best = (score, name, U)
    if best is None:
        sys.exit('ERRO: a peca nao cabe na mesa da Kobra 3 Max (426x420x500 mm) em nenhuma orientacao.')
    return best[2], best[1]


def write_stl(T, path):
    T = T - T.reshape(-1, 3).min(0)
    N = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
    rec = np.zeros(len(T), dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('a', '<u2')]))
    rec['n'] = N
    rec['v'] = T.reshape(-1, 9)
    with open(path, 'wb') as f:
        f.write(b'k3max'.ljust(80, b' '))
        f.write(struct.pack('<I', len(T)))
        f.write(rec.tobytes())
    return T


def thumbnail_png(T, w, h):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    step = max(1, len(T) // 40000)
    S = T[::step]
    N = np.cross(S[:, 1] - S[:, 0], S[:, 2] - S[:, 0])
    N /= np.linalg.norm(N, axis=1, keepdims=True) + 1e-12
    light = np.array([0.4, -0.6, 0.7]) / np.linalg.norm([0.4, -0.6, 0.7])
    sh = 0.35 + 0.65 * np.abs(N @ light)
    fig = plt.figure(figsize=(w / 100, h / 100), dpi=100)
    ax = fig.add_axes([0, 0, 1, 1], projection='3d')
    pc = Poly3DCollection(S, edgecolor='none')
    pc.set_facecolor(np.c_[sh * 0.2, sh * 0.6, sh * 0.95])
    ax.add_collection3d(pc)
    lo, hi = T.reshape(-1, 3).min(0), T.reshape(-1, 3).max(0)
    r = (hi - lo).max() / 2
    c = (hi + lo) / 2
    for setlim, i in ((ax.set_xlim, 0), (ax.set_ylim, 1), (ax.set_zlim, 2)):
        setlim(c[i] - r, c[i] + r)
    ax.view_init(35, -60)
    ax.set_axis_off()
    buf = io.BytesIO()
    fig.savefig(buf, format='png', transparent=True)
    plt.close(fig)
    return buf.getvalue()


# ---------------------------------------------------------------- perfil
def pct(v):
    return float(str(v).rstrip('%'))


def first(v):
    return v[0] if isinstance(v, list) else v


def build_config(args, use_supports):
    m = json.load(open(os.path.join(PROFILES, 'machine.json')))
    p = json.load(open(os.path.join(PROFILES, 'process.json')))
    f = json.load(open(os.path.join(PROFILES, f'filament_{args.filament}.json')))
    # padrao do usuario: Creality CR-PETG (230-250 C); o perfil Anycubic PETG usa 225 C
    default_t = {'PETG': (235, 240)}.get(args.filament)
    nozzle_t = args.nozzle_temp or (default_t[0] if default_t else int(first(f['nozzle_temperature'])))
    nozzle_t0 = args.nozzle_temp0 or (args.nozzle_temp + 5 if args.nozzle_temp else
                                      default_t[1] if default_t else int(first(f['nozzle_temperature_initial_layer'])))
    bed_t = args.bed_temp or int(first(f['textured_plate_temp']))
    bed_t0 = args.bed_temp or int(first(f['textured_plate_temp_initial_layer']))
    # valores que vao para o bloco de config (formato Anycubic Slicer Next)
    p.update({'layer_height': str(args.layer), 'wall_loops': str(args.walls),
              'sparse_infill_density': f'{args.infill}%', 'enable_support': '1' if use_supports else '0',
              'support_type': 'normal(auto)', 'brim_type': 'outer_only' if args.brim else 'no_brim',
              'brim_width': str(args.brim)})
    f.update({'nozzle_temperature': [str(nozzle_t)], 'nozzle_temperature_initial_layer': [str(nozzle_t0)],
              'textured_plate_temp': [str(bed_t)], 'textured_plate_temp_initial_layer': [str(bed_t0)],
              'hot_plate_temp': [str(bed_t)], 'hot_plate_temp_initial_layer': [str(bed_t0)]})
    full = {}
    full.update(m); full.update(p); full.update(f)
    full.update({'curr_bed_type': 'Textured PEI Plate', 'printer_settings_id': m['name'],
                 'print_settings_id': p['name'], 'filament_settings_id': [f['name']]})

    fan_min, fan_max = int(first(f['fan_min_speed'])), int(first(f['fan_max_speed']))
    flow = first(f.get('filament_flow_ratio', '1'))
    vol = first(f.get('filament_max_volumetric_speed', '12'))
    density = first(f.get('filament_density', '1.24'))
    retract = first(m.get('retraction_length', '0.8'))
    zhop = first(m.get('z_hop', '0.4'))
    start = ('G9111 bedTemp=[first_layer_bed_temperature] extruderTemp=[first_layer_temperature]\n'
             'M117\n'
             '; print_bed_min = 0,0\n; print_bed_max = 426,420\n; print_bed_size = 426,420\n'
             '; first_layer_print_min = {first_layer_print_min[0]},{first_layer_print_min[1]}\n'
             '; first_layer_print_max = {first_layer_print_max[0]},{first_layer_print_max[1]}\n'
             '; first_layer_print_size = {first_layer_print_size[0]},{first_layer_print_size[1]}')
    end = m['machine_end_gcode']
    ini = {
        'printer_technology': 'FFF', 'gcode_flavor': 'klipper',
        'bed_shape': f'0x0,{BED_X}x0,{BED_X}x{BED_Y},0x{BED_Y}', 'max_print_height': MAX_Z,
        'nozzle_diameter': 0.4, 'filament_diameter': 1.75, 'use_relative_e_distances': 1,
        'autoemit_temperature_commands': 0,
        'start_gcode': start.replace('\n', '\\n'), 'end_gcode': end.replace('\n', '\\n'),
        'before_layer_change_gcode': '; BEFORE_LAYER_CHANGE [layer_num] @ [layer_z]mm',
        'layer_gcode': '; AFTER_LAYER_CHANGE [layer_num] @ [layer_z]mm',
        'machine_limits_usage': 'time_estimate_only', 'remaining_times': 1,
        'machine_max_feedrate_x': 600, 'machine_max_feedrate_y': 600,
        'machine_max_acceleration_extruding': 10000, 'machine_max_acceleration_travel': 10000,
        'retract_length': retract, 'retract_speed': 30, 'deretract_speed': 30,
        'retract_lift': zhop, 'retract_layer_change': 1, 'wipe': 1,
        'filament_type': args.filament, 'filament_density': density,
        'temperature': nozzle_t, 'first_layer_temperature': nozzle_t0,
        'bed_temperature': bed_t, 'first_layer_bed_temperature': bed_t0,
        'extrusion_multiplier': flow, 'filament_max_volumetric_speed': vol,
        'fan_always_on': 1, 'min_fan_speed': fan_min, 'max_fan_speed': fan_max,
        'disable_fan_first_layers': int(first(f.get('close_fan_the_first_x_layers', '1'))),
        'full_fan_speed_layer': int(first(f.get('full_fan_speed_layer', '3'))),
        'layer_height': args.layer, 'first_layer_height': args.layer,
        'perimeters': args.walls, 'top_solid_layers': p['top_shell_layers'],
        'bottom_solid_layers': p['bottom_shell_layers'],
        'fill_density': f'{args.infill}%', 'fill_pattern': 'gyroid',
        'support_material': 1 if use_supports else 0, 'support_material_auto': 1,
        'support_material_threshold': 45, 'support_material_style': 'snug',
        # folga = altura de camada, para o suporte nao gerar camadas intercaladas
        'support_material_contact_distance': args.layer,
        'support_material_spacing': 2.5,
        'skirts': 1, 'skirt_distance': 4, 'brim_width': args.brim, 'brim_type': 'outer_only',
        'first_layer_speed': p['initial_layer_speed'], 'perimeter_speed': p['inner_wall_speed'],
        'external_perimeter_speed': 80 if args.filament == 'PETG' else p['outer_wall_speed'],
        'infill_speed': p['sparse_infill_speed'], 'solid_infill_speed': p['internal_solid_infill_speed'],
        'top_solid_infill_speed': p['top_surface_speed'], 'support_material_speed': p['support_speed'],
        'bridge_speed': p['bridge_speed'], 'gap_fill_speed': 80, 'small_perimeter_speed': 50,
        'travel_speed': p['travel_speed'], 'default_acceleration': p['default_acceleration'],
        'first_layer_acceleration': p['initial_layer_acceleration'],
        'perimeter_acceleration': p['inner_wall_acceleration'],
        'external_perimeter_acceleration': p['outer_wall_acceleration'],
        'infill_acceleration': p['sparse_infill_acceleration'],
        'travel_acceleration': p['travel_acceleration'],
        'top_solid_infill_acceleration': p['top_surface_acceleration'],
        'seam_position': 'aligned', 'gcode_label_objects': 'firmware',
        'gcode_comments': 0,
    }
    return ini, full, float(density)


def serialize(v):
    if isinstance(v, list):
        v = ','.join(str(x) for x in v)
    return str(v).replace('\n', '\\n')


# ---------------------------------------------------------------- G-code
def to_anycubic(raw, full, T, model_name):
    body = raw.split('\n')
    stats, out_body, layers, cur_z = {}, [], 0, 0.0
    in_cfg = False
    for line in body:
        if line.startswith('; prusaslicer_config = begin'):
            in_cfg = True
        if in_cfg:
            if line.startswith('; prusaslicer_config = end'):
                in_cfg = False
            continue
        mm = re.match(r'; (filament used \[(mm|cm3|g)\]|estimated printing time \(normal mode\)|estimated first layer printing time \(normal mode\)|total filament used \[g\]) = (.*)', line)
        if mm:
            stats[mm.group(1)] = mm.group(3).strip()
            continue
        if line.startswith('; generated by') or line.startswith('; thumbnail') or line.startswith('; total filament'):
            continue
        out_body.append(line)
        if line == ';LAYER_CHANGE':
            layers += 1
        elif line.startswith(';Z:'):
            z = float(line[3:])
            out_body.append(f'; CHANGE_LAYER\n; Z_HEIGHT: {z:g}\n; LAYER_HEIGHT: {z - cur_z:g}')
            cur_z = z
    est = stats.get('estimated printing time (normal mode)', '0s')
    mm_used = float(stats.get('filament used [mm]', '0'))
    cm3 = float(stats.get('filament used [cm3]', '0'))
    grams = float(stats.get('filament used [g]', '0'))
    dens = first(full.get('filament_density', '1.24'))
    zmax = T[:, :, 2].max()
    now = datetime.datetime.now()

    hdr = ['; HEADER_BLOCK_START',
           f'; generated by {APP} on {now:%Y-%m-%d} at {now:%H:%M:%S}',
           f'; model printing time: {est}; total estimated time: {est}',
           f'; total layer number: {layers}',
           f'; total filament length [mm] : {mm_used:.2f}',
           f'; total filament volume [cm^3] : {cm3 * 1000:.2f}',
           f'; total filament weight [g] : {grams:.2f}',
           f'; filament_density: {dens}',
           '; filament_diameter: 1.75',
           f'; max_z_height: {zmax:.2f}',
           f'; estimated printing time (normal mode) = {est}',
           '; HEADER_BLOCK_END', '']
    thumbs = ['; THUMBNAIL_BLOCK_START']
    for w, h in ((230, 110), (512, 512)):
        b64 = base64.b64encode(thumbnail_png(T, w, h)).decode()
        thumbs.append(f'; thumbnail begin {w}x{h} {len(b64)}')
        thumbs += ['; ' + b64[i:i + 78] for i in range(0, len(b64), 78)]
        thumbs.append('; thumbnail end')
    thumbs += ['; THUMBNAIL_BLOCK_END', '']
    tail = ['; EXECUTABLE_BLOCK_END', '',
            f'; filament used [mm] = {mm_used:.2f}',
            f'; filament used [cm3] = {cm3:.2f}',
            f'; filament used [g] = {grams:.2f}',
            '; filament cost = 0.00',
            f'; total filament used [g] = {grams:.2f}',
            '; total filament cost = 0.00',
            f'; total layers count = {layers}',
            f'; estimated printing time (normal mode) = {est}', '',
            '; CONFIG_BLOCK_START']
    for k in sorted(full):
        line = f'; {k} = {serialize(full[k])}'
        if not line.startswith(BAD_PREFIXES):
            tail.append(line)
    tail += ['; CONFIG_BLOCK_END', '']
    text = '\n'.join(hdr + thumbs + ['; EXECUTABLE_BLOCK_START'] + out_body + tail)
    return text, dict(layers=layers, est=est, grams=grams, meters=mm_used / 1000)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('model')
    ap.add_argument('--filament', choices=['PETG', 'PLA'], default='PETG')
    ap.add_argument('--out')
    ap.add_argument('--infill', type=int, default=20)
    ap.add_argument('--walls', type=int, default=3)
    ap.add_argument('--layer', type=float, default=0.2)
    ap.add_argument('--brim', type=float, default=5)
    ap.add_argument('--supports', choices=['auto', 'on', 'off'], default='auto')
    ap.add_argument('--nozzle-temp', type=int)
    ap.add_argument('--nozzle-temp0', type=int)
    ap.add_argument('--bed-temp', type=int)
    ap.add_argument('--orient', choices=['auto'] + list(ROTATIONS), default='auto')
    args = ap.parse_args()
    if not shutil.which('prusa-slicer'):
        sys.exit('ERRO: prusa-slicer nao instalado (apt-get install -y prusa-slicer xvfb).')

    T, rot = orient(load_mesh(args.model), args.orient)
    work = tempfile.mkdtemp(prefix='k3max_')
    stl = os.path.join(work, 'modelo.stl')
    T = write_stl(T, stl)
    size = np.ptp(T.reshape(-1, 3), axis=0)
    contact, hang = contact_and_overhang(T)
    use_supports = bool(args.supports == 'on' or (args.supports == 'auto' and hang > 50))

    ini, full, _ = build_config(args, use_supports)
    ini_path = os.path.join(work, 'k3max.ini')
    with open(ini_path, 'w') as fh:
        fh.write(''.join(f'{k} = {v}\n' for k, v in ini.items()))
    raw_path = os.path.join(work, 'raw.gcode')
    cmd = ['prusa-slicer', '--export-gcode', '--load', ini_path, '--center', f'{BED_X / 2},{BED_Y / 2}',
           '--output', raw_path, stl]
    if shutil.which('xvfb-run'):
        cmd = ['xvfb-run', '-a'] + cmd
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(raw_path):
        sys.exit('ERRO ao fatiar:\n' + r.stdout[-2000:] + r.stderr[-2000:])

    name = os.path.splitext(os.path.basename(args.model))[0]
    out = args.out or os.path.join(os.path.dirname(os.path.abspath(args.model)), f'{name}_K3Max_{args.filament}.gcode')
    text, info = to_anycubic(open(raw_path).read(), full, T, name)
    with open(out, 'w', newline='\n') as fh:
        fh.write(text)
    warn = [l for l in (r.stdout + r.stderr).splitlines() if 'warning' in l.lower() or 'consider' in l.lower()]
    print(json.dumps({'gcode': out, 'orientacao': rot, 'tamanho_mm': [round(float(x), 1) for x in size],
                      'area_apoio_mm2': int(contact), 'area_pendente_mm2': int(hang),
                      'suportes': use_supports, 'camadas': info['layers'], 'tempo': info['est'],
                      'filamento_g': round(info['grams']), 'filamento_m': round(info['meters'], 1),
                      'avisos_fatiador': warn}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
