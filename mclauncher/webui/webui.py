
# EDIT ON 07/29/23

import json
import os
import threading

from nicegui import ui

from ..core.launch import quickstart
from ..core.utils import *
from ..core.versions import VersionDecoder, VersionDecoder2

cwd = os.getcwd()
__version__ = '0.2' 

#temporary dummy version list
versions_addable=['dummy version 1','dummy version 2','dummy version 3','dummy version 4']

# os.system('mkdir lnxt')

try:
    with open("versions.json", "r") as f:
        versions = json.loads(f.read(), object_hook=VersionDecoder2)
        f.seek(0)
        version2 = json.loads(f.read(), object_hook=VersionDecoder)
        version_dict = dict(zip(versions, version2))
        # print(version_dict)
        print('[INFO] Config loaded.')
except FileNotFoundError:
    print('[WARN] Config file not detected.')

#Game tracking loop
def mc_loop(realversion, footer, launch_bt, start2, logs, endbt,closebt,display,username,mslogin):
    def real():
        process = quickstart(minecraft_version=realversion,username=username,mslogin=mslogin)
        endbt.enable()
        closebt.disable()
        display.on_text_change('Minecraft运行中')
        while True:
            # time.sleep(1)
            if process.poll() is not None:
                break
            try:
                ln = process.stdout.readline()
                print(ln.decode(), end="")
                logs.push(ln.decode().strip())
            except:
                with ui.dialog() as dialog, ui.card():
                    with ui.column():
                        def reload_webui():
                            ui.html('<meta http-equiv="refresh" content="0">')
                        ui.label('错误').style('color: #6E93D6; font-size: 200%; font-weight: 300')
                        ui.label('LauncherNext 在侦测Minecraft主循环处发生了一个错误。')
                        ui.label('如果你在本地运行，请检查控制台(不是页面内的logs)输出。')
                        ui.label('如果你在访问远程启动器，请提醒服务器提供商这个错误。')
                        ui.label('重载LauncherNext.webUI可能会解决问题，但会丢失与当前Minecraft实例的侦测。')
                        with ui.row():
                            ui.button('重载webUI模块', on_click=reload_webui)
                            ui.button('继续，忽略该错误', on_click=dialog.close)
            if ln.decode().strip().endswith("Stopping!"):
                break
            #Daemon trigger inject here
        n = process.stdout.read().decode()
        print(n)
        logs.push(n)
        endbt.disable()
        closebt.enable()
        display.on_text_change('Minecraft已退出')
        #down below control code at func(close_footer)
        #footer.hide()
        #logs.clear()
        #launch_bt.visible = True
        #start2.enable()
        #start1.enable()
    return real

#Launcher webUI design
@ui.page('/')
def launch():

    def reload_webui():
        ui.html('<meta http-equiv="refresh" content="0">')

    def launch_mc(version_getter):
        footer.show()
        launch_bt.visible = False
        start = ButtonGroup()
        start.add_button(start2)
        start.add_button(start1)
        start.disable()
        # ver_name = f'"{version}"'

        #version = ver_select.value
        username=usrinput.value
        print('VAR.user="'+username+'"')
        if username == '':
            username='steve'
        print("[INFO] Setting Offline User: ", username)
        logs.push("[LauncherNext] [INFO] Setting Offline User: "+username)
        if checkms.value == True:
            mslogin=emailin.value
            print("[INFO] Using Microsoft Account ", mslogin)
            logs.push("[LauncherNext] [INFO] Using Microsoft Account "+mslogin)
        else:
            mslogin=''
        version = version_getter()
        realversion = version_dict[version]
        print("[INFO] Starting Minecraft ", version)
        logs.push("[LauncherNext] [INFO] Starting Minecraft "+version)
        # time.sleep(10)
        threading.Thread(target=mc_loop(realversion, footer, launch_bt, start, logs, endbt,closebt,display,username,mslogin)).start()

    def launch_mc_now():
        footer.show()
        launch_bt.visible = False
        start = ButtonGroup()
        start.add_button(start2)
        start.add_button(start1)
        start.disable()
        # ver_name = f'"{version}"'
        username=usrinput.value
        print('VAR.user="'+username+'"')
        if username == '':
            username='steve'
        print("[INFO] Setting Offline User: ", username)
        logs.push("[LauncherNext] [INFO] Setting Offline User: "+username)
        if checkms.value == True:
            mslogin=emailin.value
            print("[INFO] Using Microsoft Account ", mslogin)
            logs.push("[LauncherNext] [INFO] Using Microsoft Account "+mslogin)
        else:
            mslogin=''
        version = ver_select.value
        realversion = version_dict[version]
        print("[INFO] Starting Minecraft ", version)
        logs.push("[LauncherNext] [INFO] Starting Minecraft "+version)
        # time.sleep(10)
        threading.Thread(target=mc_loop(realversion, footer, launch_bt, start, logs, endbt,closebt,display,username,mslogin)).start()

    def get_launch_mc(bind_to):
        def getter():
            return bind_to.value
        def callback():
            return launch_mc(getter)
        return callback
    
    def get_launch_mc_now(bind_to):
        def getter():
            return bind_to.value
        def callback():
            return launch_mc_now()
        return callback

    def end_forcely():
        if os.name == "nt":
            os.system('taskkill /f /im java.exe')
        else:
            os.system('killall -9 java')
        print("[INFO] Killed Java")

    def close_footer():
        footer.hide()
        logs.clear()
        launch_bt.visible = True
        start2.enable() # FIXED: only enables one button, the other is still disabled
        start1.enable()

    with ui.dialog() as dialog, ui.card():
        with ui.column():
            ui.label('关于 LauncherNext').style(
                'color: #6E93D6; font-size: 200%; font-weight: 300'
            )
            ui.label('LauncherNext v' + __version__)
            ui.label('一个由Allen546和DarkstarXD共同开发的webUI轻量级Minecraft启动器。')
            ui.button('关闭', on_click=dialog.close)

    with ui.header().classes(replace='row items-center') as header:
        ui.button(icon='launch', on_click=dialog.open).props('flat color=white').tooltip(
            'LauncherNext v' + __version__
        )
        with ui.tabs() as tabs:
            ui.tab('启动')
            ui.tab('版本')
            ui.tab('添加实例')
            ui.tab('选项')

    with ui.footer(value=False).style("height:40%") as footer:
        with ui.row():
            display=ui.label('Minecraft运行中').style('color:#FFFFFF; font-size: 200%; font-weight: 300')
            ui.label('\u00a0')
            endbt=ui.button('强行终止进程',on_click=end_forcely).style('font-color:#FFFFFF')
            closebt=ui.button('关闭logs',on_click=close_footer).style('font-color:#FFFFFF')
            closebt.disable()
            endbt.enable()

        with ui.column().style("width: 100%; height: 100%"):
            # To use the progressbar(which is developing) with no actual use:
            logs = ui.log().style("width: 100%; height: 80%")
            #progressbar = ui.linear_progress(value=0).props('instant-feedback').style("width:100%;")

    with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
        launch_bt = ui.button(on_click=launch_mc_now, icon='rocket').props('fab')
        

    with ui.tab_panels(tabs, value='启动').classes('w-full'):
        with ui.tab_panel('启动'):
            ui.label('启动面板').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.label('\u00a0')  # Added some spaces through the interface
            ui.separator()
            ui.label('\u00a0')
            with ui.column():
                with ui.row():
                    with ui.card():
                        with ui.column():
                            ui.label('简易启动')
                            ver_select2 = ui.select(versions, value=str(versions[0]))
                            start1 = ui.button("启动Minecraft", on_click=get_launch_mc_now(ver_select2))
                            # ui.button('管理登录', on_click=login).tooltip('管理Littleskin登录通行证')
                            # chk_var = ui.checkbox('补全文件 (会拖慢启动速度，但能解决大部分问题)')
                    ui.label('\u00a0')
                    with ui.card():
                        with ui.column():
                            ui.label('自定义启动')
                            ver_select = ui.select(versions, value=str(versions[0]))
                            start2 = ui.button("启动Minecraft", on_click=get_launch_mc(ver_select))
                            # ui.button('管理登录', on_click=login).tooltip('管理Littleskin登录通行证')
                            # chk_var = ui.checkbox('补全文件 (会拖慢启动速度，但能解决大部分问题)')
                ui.label('\u00a0')
                with ui.card():
                    with ui.row():
                        with ui.card():
                            with ui.column():
                                checkms = ui.checkbox('启用Microsoft账户登录')
                            ui.label('启动器将在你下次启动MC时要求授权你的Microsoft账户。').bind_visibility_from(checkms, 'value')
                            emailin=ui.input('email').bind_visibility_from(checkms, 'value')
                        with ui.card():
                            with ui.column():
                                checkemail = ui.checkbox('启用Littleskin登录')
                                ui.label('免费的Authlib注入登录方式').bind_visibility_from(checkemail, 'value')
                                ui.input('email或用户名').bind_visibility_from(checkemail, 'value')
                                ui.input('密码',password=True,password_toggle_button=True).bind_visibility_from(checkemail, 'value')
                                ui.button('保存/刷新 登录Token').bind_visibility_from(checkemail, 'value')
                                ui.link('注册Littleskin账户','https://littleskin.cn/auth/register').bind_visibility_from(checkemail, 'value')
                                ui.link('浏览皮肤库','https://littleskin.cn/skinlib').bind_visibility_from(checkemail, 'value')
                        with ui.card():
                            with ui.column():
                                checkoffline = ui.checkbox('启用离线登录')
                                usrinput=ui.input('玩家代号').bind_visibility_from(checkoffline, 'value')
                                ui.label('使用该方法登录时，部分Minecraft功能将无法使用。').bind_visibility_from(checkoffline, 'value')
                    ui.label('Tip: 若你没有选定任意一个登录选项，启动器将自动以玩家代号为Steve离线启动Minecraft。')
                    ui.label('如果你选择了多个登录方式，启动器将依次使用Microsoft账户-Littleskin账户-离线登录的顺序尝试登录Minecraft。')                    
                    ui.link('购买正版账户','https://www.xbox.com/zh-cn/games/store/minecraft-java-bedrock-edition-for-pc/9nxp44l49shj')
                    ui.link('还在用Mojang账户?点此迁移到Microsoft账户','https://www.minecraft.net/zh-hans/account-security')
        with ui.tab_panel('版本'):
            ui.label('版本管理').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.label('\u00a0')  # Added some spaces through the interface
            ui.separator()
            ui.label('\u00a0')
            columns = [
    {'name': 'name', 'label': '版本名称', 'field': 'name', 'required': True, 'align': 'left'},
    {'name': 'type', 'label': '类型', 'field': 'class', 'required': True, 'sortable': True},
    #{'name': 'operation', 'label': '操作', 'field': 'operation', 'required': True, 'sortable': False},
]
            rows = [{'name': version.split()[1], 'class': version.split()[0]} for version in versions]

            with ui.column():
                ui.table(columns=columns, rows=rows, row_key='name')

        with ui.tab_panel('添加实例'):
            ui.label('添加实例').style('color: #6E93D6; font-size: 200%; font-weight: 300')
            ui.label('\u00a0')  # Added some spaces through the interface
            ui.separator()
            ui.label('\u00a0')
            with ui.column():
                with ui.card():
                    with ui.column():
                        ui.label('添加新实例')
                        ver_select2 = ui.select(versions_addable, value=str(versions_addable[0]))
                        addbt = ui.button("添加到版本列表")
        with ui.tab_panel('选项'):
            dark = ui.dark_mode()
            with ui.card():
                ui.label('重载').style(
                    'color: #6E93D6; font-size: 200%; font-weight: 300'
                )
                with ui.column():
                    ui.label('如果LauncherNext出现问题或运行不稳定，可以点击以下按钮重载webUI模块来解决。')
                    ui.label('请确认你没有运行任何Minecraft实例，再进行此操作。')
                    ui.button('重载webUI', on_click=reload_webui)
            ui.label('\u00a0')
            with ui.card():
                ui.label('UI个性化').style(
                    'color: #6E93D6; font-size: 200%; font-weight: 300'
                )
                ui.label('切换主题:')
                ui.button('暗色', on_click=dark.enable)
                ui.button('亮色', on_click=dark.disable)
                ui.separator()
                ui.label('切换色调:')
                ui.button('默认蓝', on_click=lambda: ui.colors())
                ui.button('低调灰', on_click=lambda: ui.colors(primary='#555'))
            ui.label('\u00a0')
            with ui.card():
                ui.label('Minecraft实例').style(
                    'color: #6E93D6; font-size: 200%; font-weight: 300'
                )
                with ui.column():
                    switch1 = ui.switch('启用版本隔离')
                    switch2 = ui.switch('强制使用指定Java')
                    switch3 = ui.switch('DUMMY SWITCH')
                    switch4 = ui.switch('switch me')
                    switch5 = ui.switch('switch me')
                    switch6 = ui.switch('switch me')
            ui.label('\u00a0')
            with ui.card():
                ui.label('启动选项').style(
                    'color: #6E93D6; font-size: 200%; font-weight: 300'
                )
                with ui.column():
                    ui.label('Daemon侦测循环频率(单位:s)(目前没用)')
                    with ui.row():
                        slider = ui.slider(min=0, max=5, value=1)
                        ui.label().bind_text_from(slider, 'value')
                    switch1 = ui.switch('1')
                    switch2 = ui.switch('2')
                    switch3 = ui.switch('3')
                    switch4 = ui.switch('4')
                    switch5 = ui.switch('A')
                    switch6 = ui.switch('B')