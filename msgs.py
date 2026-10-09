# тексты ошибок как в CPython (выполняется внутри build5.py, использует rep и s)
import re as _re
_p = _re.compile(r"throw new Sk\.builtin\.TypeError\(\"cannot concatenate 'str' and '\"\+\s*Sk\.abstr\.typeName\(a\)\+\"' objects\"\)")
assert len(_p.findall(s)) == 1
s = _p.sub(lambda m: 'throw new Sk.builtin.TypeError("can only concatenate str (not \\""+Sk.abstr.typeName(a)+"\\") to str")', s)
rep('a=this.list$inRange(a,"pop index out of range");', 'if(!this.v.length)throw new Sk.builtin.IndexError("pop from empty list");a=this.list$inRange(a,"pop index out of range");')
_old = 'throw new Sk.builtin.ValueError("min() arg is an empty sequence")'
assert s.count(_old) == 2
s = s.replace(_old, 'throw new Sk.builtin.ValueError("min() iterable argument is empty")', 1).replace(_old, 'throw new Sk.builtin.ValueError("max() iterable argument is empty")', 1)
rep('''throw new Sk.builtin.TypeError("'"+Sk.abstr.typeName(a)+"' does not support item assignment")''', '''throw new Sk.builtin.TypeError("'"+Sk.abstr.typeName(a)+"' object does not support item assignment")''')
rep('"not enough values to unpack (expected at least "+c+", got "+f.length+")"', '"not enough values to unpack (expected "+c+", got "+f.length+")"')
rep('throw new Sk.builtin.ImportError("No module named "+a);', '''throw new Sk.builtin.ImportError("No module named '"+a+"'");''')
rep('function e(a,b){if(0===b)throw new Sk.builtin.ZeroDivisionError("integer division or modulo by zero");return Infinity===a', 'function e(a,b){if(0===b)throw new Sk.builtin.ZeroDivisionError("division by zero");return Infinity===a')

# --- цвета для функций из модулей (itertools, json, copy и т.д.)
rep("isatty');", "isatty dump load dumps loads strptime strftime isoformat total_seconds writerow writerows writeheader getvalue');\nvar TB=W('accumulate chain count cycle repeat product permutations combinations combinations_with_replacement islice groupby starmap zip_longest deepcopy reduce partial heappush heappop heapify nlargest nsmallest mean median mode stdev pprint pformat timeit getsizeof isqrt comb perm prod lcm reader writer DictReader DictWriter forward fd backward bk back left lt right rt goto setpos setposition setx sety setheading seth home circle dot stamp speed penup pu pendown pd pensize isdown pencolor fillcolor color begin_fill end_fill hideturtle ht showturtle st xcor ycor heading position pos distance towards tracer update bgcolor mainloop exitonclick done setworldcoordinates Screen Turtle sqrt cos sin radians gcd hypot atan2 floor ceil');")
rep("if(!(BI[n]||MS[n]||ML[n]||MD[n]||MT[n]||MF[n]))return ''", "if(!(BI[n]||MS[n]||ML[n]||MD[n]||MT[n]||MF[n]||TB[n]))return ''")
rep("else k=KW[t]?'kw':BI[t]?'bi':'';", "else k=KW[t]?'kw':BI[t]?'bi':(TB[t]&&/^[ \\t]*\\(/.test(c.slice(re.lastIndex)))?'bi':'';")
