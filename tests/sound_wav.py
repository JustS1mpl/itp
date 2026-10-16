"""Измерение звуков ИТП (нужны Playwright, numpy, scipy, matplotlib).
Каждый звук рисуется без динамиков (OfflineAudioContext в Chromium, без случайных вариаций) из sounds-preview.html,
сохраняется в WAV и проверяется: нулевые края, нет клиппинга, пик совпадает с целевым (pk в таблице SXD),
длительность, нет резких частот выше 6–8 кГц, согласованность громкости семейств.
Запуск из корня репозитория:
  python3 tests/mk_preview.py && python3 tests/sound_wav.py [--out папка_для_wav] [--calibrate] [--png файл.png]
--calibrate подправляет числа lv в v5/a_sound.js, чтобы пик каждого звука стал равен pk (потом заново mk_preview.py)."""
import os, sys, re, json, argparse
import numpy as np
from scipy import signal
from scipy.io import wavfile
from playwright.sync_api import sync_playwright

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 44100
ap = argparse.ArgumentParser()
ap.add_argument('--out', default=os.path.join(W, 'tests', '_wav'))
ap.add_argument('--calibrate', action='store_true')
ap.add_argument('--png', default=os.path.join(W, 'tests', 'sound_spectrograms.png'))
ap.add_argument('--quiet', action='store_true')
ap.add_argument('--json', default='')
args = ap.parse_args()

# предельная длительность по уровню −50 дБ (мс) каждого звука-варианта (имя без номера варианта: tap_1 → tap)
LIMIT = {'tap': 140, 'nav': 150, 'toggle_on': 150, 'toggle_off': 150, 'sheet_open': 200, 'sheet_close': 200, 'correct': 350, 'wrong': 350,
         'hint': 330, 'xp': 90, 'complete': 700, 'streak': 520, 'achievement': 1000, 'run': 110, 'error': 260, 'key': 80, 'del': 80}
TAPF = ('tap', 'nav', 'toggle_on', 'toggle_off', 'run')

def base(n):
    return n.rsplit('_', 1)[0]

STRESS = """(function(){
  var sr=44100,c=new OfflineAudioContext(1,sr*3,sr),x=sxBuild(c,false);x.mst.gain.value=1;
  var seq=[],i;for(i=0;i<40;i++)seq.push([.05+i*.04,'tap_1']);                  /* 40 касаний, по одному каждые 40 мс */
  seq.push([.3,'correct_1'],[.32,'complete_1'],[.34,'achievement_1'],[.36,'wrong_1'],[.4,'xp_1'],[.42,'sheet_open_1'],[.5,'streak_1'],[.52,'complete_1']);
  var pits=[],maxv=0,gains=[],errs=0;
  var p=Promise.resolve();
  seq.sort(function(a,b){return a[0]-b[0]});
  seq.forEach(function(e){var t=Math.round(e[0]*sr/128)*128/sr;
    c.suspend(t).then(function(){try{var v=sxFire(x,e[1],{k:2});if(e[1].indexOf('tap')===0)pits.push(v.pit);maxv=Math.max(maxv,x.voices.length)}catch(er){errs++}c.resume()})});
  return c.startRendering().then(function(b){return{pits:pits,maxv:maxv,errs:errs,s:Array.from(b.getChannelData(0))}})})()"""


def get_variants(pg):
    names = pg.evaluate("Object.keys(SXD)")
    v = [(n, None, n) for n in names]
    v += [('xp_1', {'k': k}, 'xp_k%d' % k) for k in (0, 2, 5, 9)]
    return v


def kweight(x, sr=SR):
    """ITU-R BS.1770: K-взвешивание (коэффициенты для 48 кГц), вход пересчитывается до 48 кГц"""
    y = signal.resample_poly(x, 160, 147)
    b1 = [1.53512485958697, -2.69169618940638, 1.19839281085285]; a1 = [1.0, -1.69065929318241, 0.73248077421585]
    b2 = [1.0, -2.0, 1.0]; a2 = [1.0, -1.99004745483398, 0.99007225036621]
    return signal.lfilter(b2, a2, signal.lfilter(b1, a1, y))


def loud_stats(x):
    y = kweight(x)
    sr = 48000
    pad = np.concatenate([y, np.zeros(sr)])
    w = int(.4 * sr); h = int(.05 * sr)
    m = [np.mean(pad[i:i + w] ** 2) for i in range(0, len(y), h)]
    mom = -0.691 + 10 * np.log10(max(m) + 1e-12)           # момент 400 мс (макс.)
    w1 = int(.1 * sr)
    s1 = [np.mean(pad[i:i + w1] ** 2) for i in range(0, len(y), int(.01 * sr))]
    l100 = -0.691 + 10 * np.log10(max(s1) + 1e-12)          # лучшие 100 мс
    return mom, l100


def analyse(n, x):
    pk = np.max(np.abs(x))
    pkdb = 20 * np.log10(pk + 1e-12)
    idx = np.where(np.abs(x) > pk * 10 ** (-50 / 20))[0]
    dur = (idx[-1] + 1) / SR * 1000 if len(idx) else 0
    idx40 = np.where(np.abs(x) > pk * 10 ** (-40 / 20))[0]
    dur40 = (idx40[-1] + 1) / SR * 1000 if len(idx40) else 0
    X = np.abs(np.fft.rfft(x * np.hanning(len(x)))) ** 2
    f = np.fft.rfftfreq(len(x), 1 / SR)
    tot = X.sum() + 1e-30
    hi6 = 10 * np.log10(X[f > 6000].sum() / tot + 1e-30)
    hi8 = 10 * np.log10(X[f > 8000].sum() / tot + 1e-30)
    cen = (X * f).sum() / tot
    mom, l100 = loud_stats(x)
    tailabs = np.abs(x[-64:]).max()
    return dict(pk=pkdb, dur=dur, dur40=dur40, hi6=hi6, hi8=hi8, cen=cen, mom=mom, l100=l100, first=abs(x[0]), tail=tailabs, lastnz=int(np.nonzero(x)[0][-1]) if np.any(x) else 0)


def run():
    os.makedirs(args.out, exist_ok=True)
    exe = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=exe if os.path.exists(exe) else None, args=['--no-sandbox'])
        pg = b.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('file://' + os.path.join(W, 'sounds-preview.html'))
        pg.wait_for_timeout(500)
        meta = pg.evaluate("(function(){var o={};Object.keys(SXD).forEach(function(k){o[k]={pk:SXD[k].pk,lv:SXD[k].lv,dur:SXD[k].dur}});return o})()")
        res = {}
        data = {}
        for n, a, label in get_variants(pg):
            arr = pg.evaluate("sxRender(%s,%s,44100).then(function(b){return Array.from(b)})" % (json.dumps(n), json.dumps(a)))
            x = np.array(arr, dtype=np.float64)
            data[label] = x
            res[label] = analyse(n, x)
            wavfile.write(os.path.join(args.out, label + '.wav'), SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))
        st = pg.evaluate(STRESS)
        b.close()
    assert not errs, errs

    if args.calibrate:
        s = open(os.path.join(W, 'v5/a_sound.js'), encoding='utf-8').read()
        for n in meta:
            d = res[n]['pk'] - meta[n]['pk']
            new = round(meta[n]['lv'] - d, 2)
            pat = re.compile(r'(^  %s:\{[^\n]*?\bpk:-?[\d.]+,lv:)(-?[\d.]+)' % re.escape(n), re.M)
            assert pat.search(s), n
            s = pat.sub(lambda m: m.group(1) + ('%g' % new), s, count=1)
        open(os.path.join(W, 'v5/a_sound.js'), 'w', encoding='utf-8').write(s)
        print('lv обновлены; запусти python3 tests/mk_preview.py и проверку ещё раз')
        return 0

    if args.json:
        json.dump({k: {a: float(b) for a, b in v.items()} for k, v in res.items()}, open(args.json, 'w'), ensure_ascii=False)
    bad = []

    def ok(c, m):
        if not c:
            bad.append(m)
        if not args.quiet or not c:
            print(('  ✓ ' if c else '  ✗ ') + m)

    print('%-10s %6s %6s %7s %7s %6s %7s %7s %6s' % ('звук', 'пик', 'цель', 'мс(−50)', 'мс(−40)', 'центр', '>6к,дБ', 'M400', 'L100'))
    for label, r in res.items():
        n = label if label in meta else 'xp_1'
        tg = meta[n]['pk']
        print('%-10s %6.1f %6.1f %7.0f %7.0f %6.0f %7.1f %7.1f %6.1f' % (label, r['pk'], tg, r['dur'], r['dur40'], r['cen'], r['hi6'], r['mom'], r['l100']))
    print()
    for label, r in res.items():
        n = label if label in meta else 'xp_1'
        ok(r['first'] == 0.0, '«%s»: первый сэмпл ровно 0' % label)
        ok(r['tail'] == 0.0, '«%s»: конец ровно 0 (последний ненулевой сэмпл %.0f мс из %.0f)' % (label, r['lastnz'] / 44.1, len(data[label]) / 44.1))
        ok(r['pk'] < -12, '«%s»: нет клиппинга, пик %.1f дБ' % (label, r['pk']))
        if label in meta:
            ok(abs(r['pk'] - meta[n]['pk']) <= .5, '«%s»: пик %.1f дБ близок к целевому %.1f' % (label, r['pk'], meta[n]['pk']))
        else:
            ok(abs(r['pk'] - meta[n]['pk']) <= 2.5, '«%s»: пик варианта %.1f дБ не уходит от целевого %.1f больше чем на 2,5 дБ' % (label, r['pk'], meta[n]['pk']))
        ok(r['dur'] <= LIMIT[base(n)], '«%s»: длительность %.0f мс ≤ %d мс' % (label, r['dur'], LIMIT[base(n)]))
        ok(r['hi6'] < -45, '«%s»: энергия выше 6 кГц %.1f дБ от общей (< −45)' % (label, r['hi6']))
        ok(r['hi8'] < -55, '«%s»: энергия выше 8 кГц %.1f дБ от общей (< −55)' % (label, r['hi8']))
    # общие требования
    tapn = [n for n in meta if base(n) in TAPF]
    taps = [res[n]['pk'] for n in tapn]
    mt = float(np.mean(taps))
    ok(-26 <= min(taps) and max(taps) <= -22.2, 'касания, панель, переключатели, запуск: пики %.1f…%.1f дБ в диапазоне −26…−22' % (min(taps), max(taps)))
    loud = max(r['pk'] for n, r in res.items() if n in meta)
    ok(-18.6 <= loud <= -16, 'самый громкий звук: пик %.1f дБ в диапазоне −18,6…−16' % loud)
    ok(loud - mt <= 6.5, 'самый громкий звук громче среднего касания на %.1f дБ (≤ 6,5)' % (loud - mt))
    # согласованность громкости: лучшие 100 мс (K-взвешивание). Чередующиеся варианты одного события не различаются больше чем на 2 дБ
    for ev in sorted(set(base(n) for n in meta)):
        vs = [res[n]['l100'] for n in meta if base(n) == ev]
        ok(max(vs) - min(vs) <= 2.0, 'варианты «%s» одной громкости: разброс L100 %.1f дБ (≤ 2)' % (ev, max(vs) - min(vs)))
    key = [res[n]['l100'] for n in tapn]
    mel = [res[n]['l100'] for n in meta if base(n) in ('correct', 'hint', 'complete', 'streak', 'achievement')]
    print('\nгромкость L100 (LUFS, лучшие 100 мс): касания и т. п. %.1f…%.1f, мелодии %.1f…%.1f, достижение %.1f' % (min(key), max(key), min(mel), max(mel), res['achievement_1']['l100']))
    for w in ('wrong_1', 'wrong_2', 'wrong_3'):
        ok(res[w]['l100'] <= min(res['correct_1']['l100'], res['correct_2']['l100']) + .5, '«%s» не громче «верно»' % w)
        for e in ('error_1', 'error_2'):
            ok(res[e]['l100'] < res[w]['l100'] + .5, '«%s» (ошибка в коде) не громче «%s»' % (e, w))
    ok(max(res['sheet_open_1']['l100'], res['sheet_close_1']['l100']) < max(key) - 2, 'окна тише касаний')
    ok(max(res['key_1']['pk'], res['del_1']['pk']) < mt - 10, 'печать и стирание тише касания не менее чем на 10 дБ')
    ok(res['xp_1']['pk'] < min(taps) and res['xp_2']['pk'] < min(taps), 'тик опыта тише касания')
    ok(res['xp_k9']['cen'] < 1600, 'верхний предел тика опыта %.0f Гц (нет пронзительности)' % res['xp_k9']['cen'])
    ok(abs(res['xp_k5']['cen'] - res['xp_k9']['cen']) < 60, 'после шестого шага высота тика опыта не растёт')
    ok(res['xp_k2']['cen'] < res['xp_k5']['cen'], 'высота тика опыта растёт со ступенями')

    # --- стресс: 40 быстрых касаний и наложение наград, гуманизация (в режиме приложения, не детерминированном)
    sx = np.array(st['s']); pits = st['pits']
    print('\nстресс: %d касаний, голосов одновременно максимум %d, пик %.1f дБ' % (len(pits), st['maxv'], 20 * np.log10(np.abs(sx).max())))
    ok(st['errs'] == 0, 'стресс-тест без исключений')
    ok(st['maxv'] <= 6, 'не больше 6 голосов одновременно (было %d)' % st['maxv'])
    ok(np.abs(sx).max() < 0.5, 'стресс: наложение звуков не даёт клиппинга (пик %.1f дБ)' % (20 * np.log10(np.abs(sx).max())))
    ok(np.abs(sx[-64:]).max() == 0.0 and np.isfinite(sx).all(), 'стресс: после всех звуков цифровая тишина, нет NaN')
    ok(max(abs(pp - 1) for pp in pits) <= .035 + 1e-9, 'высота каждого касания в пределах ±3,5 %% (от %.3f до %.3f)' % (min(pits), max(pits)))
    ok(all(abs(pits[i] - pits[i - 1]) >= .008 for i in range(1, len(pits))), 'два касания подряд никогда не звучат на одной высоте (минимальная разница %.2f %%)' % (100 * min(abs(pits[i] - pits[i - 1]) for i in range(1, len(pits)))))
    ok(len(set(round(pp, 4) for pp in pits)) > 30, 'высоты разнообразны: %d разных из %d' % (len(set(round(pp, 4) for pp in pits)), len(pits)))
    d2 = np.abs(np.diff(sx)); 
    ok(d2.max() < 0.12, 'стресс: нет скачков между соседними сэмплами (максимум %.3f)' % d2.max())

    # спектрограммы
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    names = [k for k in res if k in meta]
    cols = 7; rows = int(np.ceil(len(names) / cols))
    fig, axs = plt.subplots(rows, cols, figsize=(cols * 2.6, rows * 1.9), dpi=70)
    for ax in axs.flat:
        ax.axis('off')
    for ax, n in zip(axs.flat, names):
        x = data[n]
        f, t, S = signal.spectrogram(x, SR, nperseg=512, noverlap=448)
        ax.pcolormesh(t * 1000, f / 1000, 10 * np.log10(S + 1e-14), vmin=-130, vmax=-50, shading='auto', cmap='magma')
        ax.axhline(6, color='c', lw=.6); ax.axhline(8, color='w', lw=.6)
        ax.set_ylim(0, 12); ax.set_title('%s  %.1f дБ' % (n, res[n]['pk']), fontsize=8)
        ax.axis('on'); ax.tick_params(labelsize=6)
    fig.suptitle('Спектрограммы (кГц, мс). Линии: 6 кГц (голубая), 8 кГц (белая). Яркость выше 6 кГц должна быть тёмной', fontsize=9)
    fig.tight_layout()
    fig.savefig(args.png)
    print('спектрограммы:', args.png)
    if bad:
        print('\nНЕ ПРОШЛО (%d):' % len(bad))
        for m in bad:
            print('  -', m)
        return 1
    print('\nOK: все проверки звука пройдены (%d звуков и вариантов)' % len(res))
    return 0


sys.exit(run())
