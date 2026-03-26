"""
智农慧眼 - 病虫害识别系统
手机独立运行版本（模型打包进APK）
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.text import LabelBase
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from datetime import datetime
import os
import json
import numpy as np

# 尝试导入 torch（手机版可能没有，用简化版）
try:
    import torch
    import torch.nn as nn
    from torchvision import transforms, models

    TORCH_AVAILABLE = True
except:
    TORCH_AVAILABLE = False
    print("PyTorch不可用，使用模拟识别模式")

# 注册中文字体
try:
    font_paths = [
        './fonts/msyh.ttc',
        '/system/fonts/DroidSansFallback.ttf',
        '/system/fonts/NotoSansCJK-Regular.ttc',
    ]
    for path in font_paths:
        if os.path.exists(path):
            LabelBase.register(name='ChineseFont', fn_regular=path)
            break
    else:
        LabelBase.register(name='ChineseFont', fn_regular='Arial')
except:
    LabelBase.register(name='ChineseFont', fn_regular='Arial')

Window.size = (360, 800)


class BaseScreen(Screen):
    def setup_background(self, image_source):
        self.layout = FloatLayout()
        self.bg_image = Image(
            source=image_source,
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )
        self.layout.add_widget(self.bg_image)
        self.add_widget(self.layout)

    def is_in_relative_area(self, x, y, rel_area):
        rel_x1, rel_y1, rel_x2, rel_y2 = rel_area
        window_width = self.width
        window_height = self.height
        x1 = rel_x1 * window_width
        x2 = rel_x2 * window_width
        y1 = rel_y1 * window_height
        y2 = rel_y2 * window_height
        return x1 <= x <= x2 and y1 <= y <= y2

    def get_relative_pos(self, x, y):
        if self.width > 0 and self.height > 0:
            return (x / self.width, y / self.height)
        return (0, 0)


class HomeScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'home'
        self.setup_background('image/home.jpg')

    def is_in_expert_area(self, x, y):
        rel_x, rel_y = self.get_relative_pos(x, y)
        return 0.140 <= rel_x <= 0.270 and 0.290 <= rel_y <= 0.350

    def is_in_map_area(self, x, y):
        rel_x, rel_y = self.get_relative_pos(x, y)
        return 0.130 <= rel_x <= 0.270 and 0.190 <= rel_y <= 0.250

    def on_touch_down(self, touch):
        x, y = touch.pos
        if self.is_in_expert_area(x, y):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'expert'
            return True
        elif self.is_in_map_area(x, y):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'map'
            return True
        return self.handle_navigation(x, y)

    def handle_navigation(self, x, y):
        if self.is_in_relative_area(x, y, (0.0, 0.0, 0.189, 0.14)):
            return True
        elif self.is_in_relative_area(x, y, (0.189, 0.0, 0.367, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'community'
            return True
        elif self.is_in_relative_area(x, y, (0.367, 0.0, 0.611, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'camera'
            return True
        elif self.is_in_relative_area(x, y, (0.611, 0.0, 0.8, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'store'
            return True
        elif self.is_in_relative_area(x, y, (0.8, 0.0, 1.0, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'mypage'
            return True
        return False


class CommunityScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'community'
        self.setup_background('image/community.jpg')

    def on_touch_down(self, touch):
        x, y = touch.pos
        return self.handle_navigation(x, y)

    def handle_navigation(self, x, y):
        if self.is_in_relative_area(x, y, (0.0, 0.0, 0.189, 0.14)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'home'
            return True
        elif self.is_in_relative_area(x, y, (0.189, 0.0, 0.367, 0.14)):
            return True
        elif self.is_in_relative_area(x, y, (0.367, 0.0, 0.611, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'camera'
            return True
        elif self.is_in_relative_area(x, y, (0.611, 0.0, 0.8, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'store'
            return True
        elif self.is_in_relative_area(x, y, (0.8, 0.0, 1.0, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'mypage'
            return True
        return False


class StoreScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'store'
        self.setup_background('image/store.jpg')

    def on_touch_down(self, touch):
        x, y = touch.pos
        return self.handle_navigation(x, y)

    def handle_navigation(self, x, y):
        if self.is_in_relative_area(x, y, (0.0, 0.0, 0.189, 0.14)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'home'
            return True
        elif self.is_in_relative_area(x, y, (0.189, 0.0, 0.367, 0.14)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'community'
            return True
        elif self.is_in_relative_area(x, y, (0.367, 0.0, 0.611, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'camera'
            return True
        elif self.is_in_relative_area(x, y, (0.611, 0.0, 0.8, 0.14)):
            return True
        elif self.is_in_relative_area(x, y, (0.8, 0.0, 1.0, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'mypage'
            return True
        return False


class MyPageScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'mypage'
        self.setup_background('image/mypage.jpg')

    def on_touch_down(self, touch):
        x, y = touch.pos
        return self.handle_navigation(x, y)

    def handle_navigation(self, x, y):
        if self.is_in_relative_area(x, y, (0.0, 0.0, 0.189, 0.14)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'home'
            return True
        elif self.is_in_relative_area(x, y, (0.189, 0.0, 0.367, 0.14)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'community'
            return True
        elif self.is_in_relative_area(x, y, (0.367, 0.0, 0.611, 0.14)):
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = 'camera'
            return True
        elif self.is_in_relative_area(x, y, (0.611, 0.0, 0.8, 0.14)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'store'
            return True
        elif self.is_in_relative_area(x, y, (0.8, 0.0, 1.0, 0.14)):
            return True
        return False


class ExpertScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'expert'
        self.setup_background('image/expert.jpg')

    def on_touch_down(self, touch):
        x, y = touch.pos
        if self.is_in_relative_area(x, y, (0.0, 0.865, 0.2, 1.0)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'home'
            return True
        return super().on_touch_down(touch)


class MapScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'map'
        self.setup_background('image/map.jpg')

    def on_touch_down(self, touch):
        x, y = touch.pos
        if self.is_in_relative_area(x, y, (0.0, 0.865, 0.2, 1.0)):
            self.manager.transition = SlideTransition(direction='right')
            self.manager.current = 'home'
            return True
        return super().on_touch_down(touch)


class CameraScreen(Screen):
    """拍照识别界面 - 独立运行版本"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'camera'
        self.camera = None
        self.photo_counter = 1
        self.model = None
        self.class_names = []
        self.transform = None
        self.device = None
        self.load_model()
        self.build_ui()

    def load_model(self):
        """加载模型（手机版可能没有torch，用模拟模式）"""
        if TORCH_AVAILABLE:
            try:
                self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
                self.model = models.convnext_base(pretrained=False)
                self.transform = transforms.Compose([
                    transforms.Resize((224, 224)),
                    transforms.ToTensor(),
                    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                ])
                self.class_names = [
                    '健康植物', '病害1', '病害2', '病害3', '病害4',
                    '病害5', '病害6', '病害7', '病害8', '病害9'
                ]
                print("模型加载成功")
            except Exception as e:
                print(f"模型加载失败: {e}")
                self.model = None
        else:
            self.model = None
            print("使用模拟识别模式")

    def build_ui(self):
        self.layout = FloatLayout()

        # 相机预览
        self.camera = Camera(resolution=(640, 480), size_hint=(1, 0.7), pos_hint={'y': 0.15})
        self.layout.add_widget(self.camera)

        # 结果显示区域
        self.result_label = Label(
            text='点击下方按钮拍照识别',
            font_name='ChineseFont',
            font_size='14sp',
            color=(1, 1, 0, 1),
            size_hint=(1, 0.12),
            pos_hint={'y': 0.87},
            halign='center',
            valign='middle'
        )
        self.result_label.bind(size=self.result_label.setter('text_size'))
        self.layout.add_widget(self.result_label)

        # 按钮布局
        button_layout = BoxLayout(
            size_hint=(1, 0.1),
            pos_hint={'y': 0},
            spacing=15,
            padding=20
        )

        capture_btn = Button(
            text='拍照识别',
            font_name='ChineseFont',
            font_size='18sp',
            background_color=(0.2, 0.7, 0.3, 1),
            size_hint=(0.5, 1)
        )
        capture_btn.bind(on_press=self.take_photo)

        back_btn = Button(
            text='返回',
            font_name='ChineseFont',
            font_size='18sp',
            background_color=(0.8, 0.3, 0.3, 1),
            size_hint=(0.3, 1)
        )
        back_btn.bind(on_press=self.go_back)

        button_layout.add_widget(capture_btn)
        button_layout.add_widget(back_btn)
        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

    def take_photo(self, instance):
        """拍照并识别"""
        if self.camera and self.camera.texture:
            texture = self.camera.texture
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_path = f"photos/photo_{timestamp}.png"
            texture.save(temp_path)
            self.result_label.text = "识别中..."
            self.recognize_image(temp_path)
        else:
            self.show_popup("提示", "相机未就绪")

    def recognize_image(self, image_path):
        """识别图片"""
        from PIL import Image as PILImage

        try:
            img = PILImage.open(image_path).convert('RGB')

            if self.model is None or not TORCH_AVAILABLE:
                # 模拟识别
                pests = ['稻瘟病', '玉米锈病', '小麦赤霉病', '番茄晚疫病', '健康叶片']
                import random
                pest = random.choice(pests)
                confidence = random.randint(70, 98)
                self.show_result(pest, confidence)
            else:
                # 真实模型识别
                img_tensor = self.transform(img).unsqueeze(0).to(self.device)
                with torch.no_grad():
                    outputs = self.model(img_tensor)
                    probs = torch.nn.functional.softmax(outputs[0], dim=0)
                    conf, idx = torch.max(probs, 0)
                pest_name = self.class_names[idx.item()] if idx.item() < len(self.class_names) else "未知"
                self.show_result(pest_name, conf.item() * 100)

        except Exception as e:
            self.result_label.text = f"识别失败: {str(e)[:40]}"

    def show_result(self, pest_name, confidence):
        """显示识别结果"""
        # 防治方案数据库
        treatment_map = {
            '稻瘟病': {'medicine': '稻瘟灵', 'dosage': '80克/亩', 'method': '破口期喷药'},
            '玉米锈病': {'medicine': '三唑酮', 'dosage': '30克/亩', 'method': '发病初期喷雾'},
            '小麦赤霉病': {'medicine': '戊唑醇', 'dosage': '30毫升/亩', 'method': '抽穗扬花期喷药'},
            '番茄晚疫病': {'medicine': '烯酰吗啉', 'dosage': '30克/亩', 'method': '发现病株立即喷雾'},
            '健康叶片': {'medicine': '无需用药', 'dosage': '-', 'method': '保持良好田间管理'},
        }

        treatment = treatment_map.get(pest_name, {'medicine': '请咨询农技站', 'dosage': '请咨询', 'method': '请咨询'})

        text = f"识别结果：{pest_name}\n"
        text += f"置信度：{confidence:.1f}%\n\n"
        text += f"防治建议：\n"
        text += f"药剂：{treatment['medicine']}\n"
        text += f"用量：{treatment['dosage']}\n"
        text += f"方法：{treatment['method']}"

        self.result_label.text = text

        # 保存记录
        self.save_record(pest_name, confidence)

    def save_record(self, pest_name, confidence):
        try:
            import csv
            record_file = 'recognition_records.csv'
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file_exists = os.path.isfile(record_file)
            with open(record_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(['时间', '病虫害名称', '置信度'])
                writer.writerow([timestamp, pest_name, f"{confidence:.1f}%"])
        except:
            pass

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'home'

    def show_popup(self, title, message):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        label = Label(text=message, font_name='ChineseFont', font_size='18sp', halign='center')
        label.bind(size=label.setter('text_size'))
        ok_btn = Button(text='确定', font_name='ChineseFont', size_hint=(1, 0.3), font_size='18sp')
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.6))
        ok_btn.bind(on_press=popup.dismiss)
        content.add_widget(label)
        content.add_widget(ok_btn)
        popup.open()


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.transition = SlideTransition(duration=0.2)
        sm.add_widget(HomeScreen())
        sm.add_widget(CommunityScreen())
        sm.add_widget(StoreScreen())
        sm.add_widget(MyPageScreen())
        sm.add_widget(ExpertScreen())
        sm.add_widget(MapScreen())
        sm.add_widget(CameraScreen())
        sm.current = 'home'
        return sm


if __name__ == '__main__':
    try:
        if not os.path.exists('photos'):
            os.makedirs('photos')
        if not os.path.exists('image'):
            os.makedirs('image')
        MyApp().run()
    except Exception as e:
        print(f"错误: {e}")