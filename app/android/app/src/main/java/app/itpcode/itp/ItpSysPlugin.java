package app.itpcode.itp;

import android.graphics.Color;
import android.os.Build;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;

import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * ИТП во весь экран, как в браузере: страница рисуется и под строкой состояния, и под полосой навигации (без серых
 * полос сверху и снизу). Размеры этих полос уходят в страницу (insets → CSS-переменные --sa-top/--sa-bottom/…,
 * a_notify.js), а цвет значков на них ИТП меняет сам: светлые на тёмном экране, тёмные на светлом (bars).
 */
@CapacitorPlugin(name = "ItpSys")
public class ItpSysPlugin extends Plugin {
    private JSObject last = new JSObject();

    @Override
    public void load() {
        Window w = getActivity().getWindow();
        WindowCompat.setDecorFitsSystemWindows(w, false);
        w.setStatusBarColor(Color.TRANSPARENT);
        w.setNavigationBarColor(Color.TRANSPARENT);
        if (Build.VERSION.SDK_INT >= 29) {
            w.setStatusBarContrastEnforced(false);
            w.setNavigationBarContrastEnforced(false);
        }
        View wv = getBridge().getWebView();
        wv.setVerticalScrollBarEnabled(false);   // без серой полосы прокрутки справа
        wv.setHorizontalScrollBarEnabled(false);
        ViewCompat.setOnApplyWindowInsetsListener(wv, (v, ins) -> {
            Insets s = ins.getInsets(WindowInsetsCompat.Type.systemBars() | WindowInsetsCompat.Type.displayCutout());
            // клавиатура: во весь экран Android сам страницу не сжимает (adjustResize молчит), и клавиатура
            // перекрывала низ, в том числе панель символов. Сжимаем WebView до верха клавиатуры сами
            int ime = ins.isVisible(WindowInsetsCompat.Type.ime()) ? ins.getInsets(WindowInsetsCompat.Type.ime()).bottom : 0;
            ViewGroup.LayoutParams lp = v.getLayoutParams();
            if (lp instanceof ViewGroup.MarginLayoutParams && ((ViewGroup.MarginLayoutParams) lp).bottomMargin != ime) {
                ((ViewGroup.MarginLayoutParams) lp).bottomMargin = ime;
                v.setLayoutParams(lp);
            }
            float d = v.getResources().getDisplayMetrics().density;
            JSObject o = new JSObject();
            o.put("top", Math.round(s.top / d));
            o.put("bottom", ime > 0 ? 0 : Math.round(s.bottom / d));
            o.put("left", Math.round(s.left / d));
            o.put("right", Math.round(s.right / d));
            last = o;
            notifyListeners("insets", o, true);
            return ins;
        });
        ViewCompat.requestApplyInsets(wv);
    }

    @PluginMethod
    public void insets(PluginCall call) {
        call.resolve(last);
    }

    @PluginMethod
    public void bars(PluginCall call) {
        final boolean dark = Boolean.TRUE.equals(call.getBoolean("dark", false));
        getActivity().runOnUiThread(() -> {
            Window w = getActivity().getWindow();
            WindowInsetsControllerCompat c = WindowCompat.getInsetsController(w, w.getDecorView());
            c.setAppearanceLightStatusBars(!dark);
            c.setAppearanceLightNavigationBars(!dark);
            w.getDecorView().setBackgroundColor(dark ? 0xFF0B0A0C : 0xFFFBF7F5);
        });
        call.resolve();
    }
}
