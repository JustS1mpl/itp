from playwright.sync_api import sync_playwright
import h,t5,sys
CODE='''from turtle import *
left(90)
for i in range(3):
    forward(100)
    right(120)
dot(8, "red")
print(round(xcor()), round(ycor()))
'''
with sync_playwright() as p:
    b,ctx,pg,logs=h.open_page(p,t5.W+'out5.html',t5.ST,390,860)
    pg.wait_for_timeout(800)
    pg.evaluate("S.ec=%r;save();editor()"%CODE); pg.wait_for_timeout(300)
    pg.click('#run'); pg.wait_for_selector('.tuw',timeout=40000); pg.wait_for_timeout(2500)
    print(pg.inner_text('#tuinfo'), '|', pg.inner_text('#tun'))
    pg.screenshot(path='tu_a.png')
    pg.click('#tupt'); pg.click('#tuzi'); pg.click('#tuzi'); pg.wait_for_timeout(200)
    pg.click('#tumk'); 
    box=pg.locator('#tucv').bounding_box()
    pg.mouse.click(box['x']+box['width']/2, box['y']+box['height']/2); pg.wait_for_timeout(150)
    print(pg.inner_text('#tuinfo'), pg.inner_text('#tumn'))
    pg.screenshot(path='tu_b.png')
    pg.click('#tux'); pg.wait_for_timeout(200)
    print('closed', pg.locator('.tuw').count()==0, 'reopen', pg.locator('#tureopen').count(), pg.inner_text('#o'))
    print([l for l in logs if 'rror' in l][:5])
    b.close()
