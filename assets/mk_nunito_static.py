# Nunito: из переменного assets/nunito.b64 — шесть готовых начертаний woff2 в assets/nunito_static.json (build5.py). Нужен fonttools и brotli. Запуск из корня репозитория
import base64,io,json
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
src=base64.b64decode(open('assets/nunito.b64').read())
out={}
for w in (400,500,600,700,800,900):
    f=TTFont(io.BytesIO(src));g=instantiateVariableFont(f,{'wght':w},updateFontNames=False)
    g.flavor='woff2';b=io.BytesIO();g.save(b);out[str(w)]=base64.b64encode(b.getvalue()).decode()
    print(w,len(b.getvalue()))
json.dump(out,open('assets/nunito_static.json','w'))
