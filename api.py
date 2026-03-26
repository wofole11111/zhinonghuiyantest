from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import io
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("加载模型...")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 检查模型文件是否存在
if not os.path.exists('best_model.pth'):
    print("错误：找不到 best_model.pth，请先运行训练")
    exit()

# 创建模型结构
model = models.convnext_base(pretrained=False)

# 加载类别
if not os.path.exists('classes.json'):
    print("错误：找不到 classes.json")
    exit()

with open('classes.json', 'r', encoding='utf-8') as f:
    class_names = json.load(f)

# 修改最后一层
num_classes = len(class_names)
model.classifier[2] = nn.Linear(model.classifier[2].in_features, num_classes)

# 加载训练好的权重（只有1轮，准确率可能不高，但能用）
model.load_state_dict(torch.load('best_model.pth', map_location=device))
model = model.to(device)
model.eval()

print(f"模型加载完成！可识别 {len(class_names)} 种病虫害")
print(f"注意：只训练了1轮，准确率可能只有60%左右")

# 图片预处理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 防治方案数据库
treatment_db = {
    "Potato___Early_blight": {"medicine": "霜脲氰", "dosage": "50克/亩", "method": "发现中心病株立即用药",
                              "chinese_name": "马铃薯早疫病"},
    "Potato___Late_blight": {"medicine": "烯酰吗啉", "dosage": "30克/亩", "method": "发现病株立即喷雾",
                             "chinese_name": "马铃薯晚疫病"},
    "Potato___healthy": {"medicine": "无需用药", "dosage": "-", "method": "保持良好田间管理",
                         "chinese_name": "健康马铃薯"},
    "Tomato_Early_blight": {"medicine": "代森锰锌", "dosage": "80克/亩", "method": "发病初期喷雾",
                            "chinese_name": "番茄早疫病"},
    "Tomato_Late_blight": {"medicine": "烯酰吗啉", "dosage": "30克/亩", "method": "发现病株立即喷雾",
                           "chinese_name": "番茄晚疫病"},
    "Tomato_healthy": {"medicine": "无需用药", "dosage": "-", "method": "保持良好田间管理", "chinese_name": "健康番茄"},
    "Tomato_Leaf_Mold": {"medicine": "嘧菌酯", "dosage": "40毫升/亩", "method": "发病初期叶面喷雾",
                         "chinese_name": "番茄叶霉病"},
    "Tomato_Septoria_leaf_spot": {"medicine": "苯醚甲环唑", "dosage": "20毫升/亩", "method": "病叶率10%时防治",
                                  "chinese_name": "番茄斑枯病"},
    "Tomato_Bacterial_spot": {"medicine": "噻菌铜", "dosage": "50克/亩", "method": "发病初期喷雾",
                              "chinese_name": "番茄细菌性斑点病"},
    "Pepper__bell___healthy": {"medicine": "无需用药", "dosage": "-", "method": "保持良好田间管理",
                               "chinese_name": "健康甜椒"},
    "Tomato__Target_Spot": {"medicine": "苯醚甲环唑", "dosage": "20毫升/亩", "method": "发病初期喷雾",
                            "chinese_name": "番茄靶斑病"},
    "Tomato__Tomato_mosaic_virus": {"medicine": "抗病毒剂", "dosage": "30克/亩", "method": "发病前预防",
                                    "chinese_name": "番茄花叶病毒病"},
    "Tomato__Tomato_YellowLeaf__Curl_Virus": {"medicine": "防虫网+抗病毒剂", "dosage": "-", "method": "防治烟粉虱",
                                              "chinese_name": "番茄黄化曲叶病毒病"},
    "Tomato_Spider_mites_Two_spotted_spider_mite": {"medicine": "阿维菌素", "dosage": "20毫升/亩", "method": "叶背喷雾",
                                                    "chinese_name": "番茄红蜘蛛"},
}


def get_treatment(pest_name):
    """根据病虫害名称获取防治方案"""
    for key in treatment_db:
        if key == pest_name:
            return treatment_db[key]
    return {"medicine": "请咨询当地农技站", "dosage": "请咨询当地农技站", "method": "请咨询当地农技站",
            "chinese_name": pest_name.replace("_", " ")}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')

        image_tensor = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            confidence, predicted = torch.max(probabilities, 0)

        pest_name = class_names[predicted.item()]
        confidence_score = confidence.item() * 100
        treatment = get_treatment(pest_name)

        return {
            "success": True,
            "pest_name": treatment["chinese_name"],
            "confidence": round(confidence_score, 2),
            "treatment": treatment
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


@app.get("/")
async def root():
    return {"message": "病虫害识别API已启动"}


if __name__ == "__main__":
    import uvicorn

    print("启动API服务...")
    print("访问 http://127.0.0.1:8000 查看状态")
    uvicorn.run(app, host="127.0.0.1", port=8000)