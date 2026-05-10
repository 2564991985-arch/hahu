#!/usr/bin/env python3
"""
郑州市月影金沙小区基坑支护设计 CAD 绘图脚本
基于论文设计参数绘制大样图、剖面图和细部设计
"""

import sys
import math

# 尝试导入 pyautocad
try:
    from pyautocad import Autocad, APoint
    acad = Autocad(create_if_not_exists=True)
except ImportError:
    print("未安装 pyautocad 库，正在安装...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautocad"])
    from pyautocad import Autocad, APoint
    acad = Autocad(create_if_not_exists=True)

# ==================== 设计参数（基于论文）====================
# 基坑尺寸
PIT_WIDTH = 110000  # 基坑宽度 110m (mm)
PIT_LENGTH = 160000  # 基坑长度 160m (mm)
PIT_DEPTH = 8000  # 基坑开挖深度 8.0m (mm)

# 地下连续墙参数
WALL_THICKNESS = 800  # 墙体厚度 800mm
WALL_DEPTH = 14400  # 墙体深度 14.4m (开挖8m + 入土6.4m)
WALL_CONCRETE = "C30"  # 混凝土强度
WALL_REBAR = "HRB400"  # 钢筋等级

# 导墙参数
GUIDEWALL_THICKNESS = 150  # 导墙厚度 150mm
GUIDEWALL_DEPTH = 1500  # 导墙深度 1.5m
GUIDEWALL_HEIGHT = 100  # 导墙高出地面 10cm

# 降水参数
WATER_LEVEL = -5000  # 地下水位 -5.0m
WELL_SPACING = 20000  # 降水井间距 20m
WELL_DEPTH = 9700  # 井深 9.7m

def clear_drawing():
    """清空当前图纸"""
    try:
        acad.model.RemoveAll()
        print("已清空当前图纸")
    except:
        pass

def draw_plan_view():
    """绘制平面图"""
    print("绘制基坑平面图...")
    
    # 设置绘图区域
    acad.model.AddLine(APoint(0, 0), APoint(PIT_WIDTH, 0))
    acad.model.AddLine(APoint(PIT_WIDTH, 0), APoint(PIT_WIDTH, PIT_LENGTH))
    acad.model.AddLine(APoint(PIT_WIDTH, PIT_LENGTH), APoint(0, PIT_LENGTH))
    acad.model.AddLine(APoint(0, PIT_LENGTH), APoint(0, 0))
    
    # 绘制地下连续墙（双线）
    wall_offset = WALL_THICKNESS
    # 外墙
    acad.model.AddLine(APoint(0, 0), APoint(PIT_WIDTH, 0))
    acad.model.AddLine(APoint(PIT_WIDTH, 0), APoint(PIT_WIDTH, PIT_LENGTH))
    acad.model.AddLine(APoint(PIT_WIDTH, PIT_LENGTH), APoint(0, PIT_LENGTH))
    acad.model.AddLine(APoint(0, PIT_LENGTH), APoint(0, 0))
    
    # 内墙（墙体内侧）
    acad.model.AddLine(APoint(wall_offset, wall_offset), APoint(PIT_WIDTH - wall_offset, wall_offset))
    acad.model.AddLine(APoint(PIT_WIDTH - wall_offset, wall_offset), APoint(PIT_WIDTH - wall_offset, PIT_LENGTH - wall_offset))
    acad.model.AddLine(APoint(PIT_WIDTH - wall_offset, PIT_LENGTH - wall_offset), APoint(wall_offset, PIT_LENGTH - wall_offset))
    acad.model.AddLine(APoint(wall_offset, PIT_LENGTH - wall_offset), APoint(wall_offset, wall_offset))
    
    # 绘制降水井
    well_radius = 300
    well_x = WELL_SPACING
    while well_x < PIT_WIDTH - WELL_SPACING:
        well_y = WELL_SPACING
        while well_y < PIT_LENGTH - WELL_SPACING:
            # 画圆表示降水井
            center = APoint(well_x, well_y)
            acad.model.AddCircle(center, well_radius)
            well_y += WELL_SPACING
        well_x += WELL_SPACING
    
    # 添加标注
    # 基坑尺寸标注
    acad.model.AddDimAligned(
        APoint(0, -2000), APoint(PIT_WIDTH, -2000),
        APoint(0, -3000)
    ).TextOverride = f"基坑宽度: {PIT_WIDTH/1000:.1f}m"
    
    acad.model.AddDimAligned(
        APoint(-2000, 0), APoint(-2000, PIT_LENGTH),
        APoint(-3000, 0)
    ).TextOverride = f"基坑长度: {PIT_LENGTH/1000:.1f}m"

def draw_section_view():
    """绘制剖面图"""
    print("绘制基坑剖面图...")
    
    # 绘制地面线
    acad.model.AddLine(APoint(0, 0), APoint(PIT_WIDTH, 0))
    
    # 绘制土层（简化表示）
    soil_layers = [
        {"name": "杂填土", "depth": 1200, "color": 3},
        {"name": "粉土", "depth": 2000, "color": 2},
        {"name": "粉砂", "depth": 3000, "color": 4},
        {"name": "细砂", "depth": 4000, "color": 5},
    ]
    
    current_depth = 0
    for layer in soil_layers:
        # 绘制土层分界线
        acad.model.AddLine(
            APoint(0, -current_depth),
            APoint(PIT_WIDTH, -current_depth)
        )
        current_depth += layer["depth"]
    
    # 绘制基坑开挖线
    acad.model.AddLine(
        APoint(WALL_THICKNESS, -PIT_DEPTH),
        APoint(PIT_WIDTH - WALL_THICKNESS, -PIT_DEPTH)
    )
    
    # 绘制地下连续墙
    # 左墙
    acad.model.AddLine(APoint(0, 0), APoint(0, -WALL_DEPTH))
    acad.model.AddLine(APoint(WALL_THICKNESS, 0), APoint(WALL_THICKNESS, -WALL_DEPTH))
    acad.model.AddLine(APoint(0, -WALL_DEPTH), APoint(WALL_THICKNESS, -WALL_DEPTH))
    
    # 右墙
    acad.model.AddLine(APoint(PIT_WIDTH, 0), APoint(PIT_WIDTH, -WALL_DEPTH))
    acad.model.AddLine(APoint(PIT_WIDTH - WALL_THICKNESS, 0), APoint(PIT_WIDTH - WALL_THICKNESS, -WALL_DEPTH))
    acad.model.AddLine(APoint(PIT_WIDTH, -WALL_DEPTH), APoint(PIT_WIDTH - WALL_THICKNESS, -WALL_DEPTH))
    
    # 绘制导墙
    acad.model.AddLine(APoint(0, GUIDEWALL_HEIGHT), APoint(WALL_THICKNESS, GUIDEWALL_HEIGHT))
    acad.model.AddLine(APoint(0, GUIDEWALL_HEIGHT + GUIDEWALL_DEPTH), APoint(WALL_THICKNESS, GUIDEWALL_HEIGHT + GUIDEWALL_DEPTH))
    
    # 绘制地下水位线（虚线）
    water_line = acad.model.AddLine(APoint(0, WATER_LEVEL), APoint(PIT_WIDTH, WATER_LEVEL))
    water_line.Linetype = "DASHED"
    
    # 绘制降水井
    well_x = PIT_WIDTH / 2
    acad.model.AddLine(
        APoint(well_x - 300, -WELL_DEPTH),
        APoint(well_x + 300, -WELL_DEPTH)
    )
    acad.model.AddLine(
        APoint(well_x - 300, 0),
        APoint(well_x - 300, -WELL_DEPTH)
    )
    acad.model.AddLine(
        APoint(well_x + 300, 0),
        APoint(well_x + 300, -WELL_DEPTH)
    )
    
    # 添加标注
    # 开挖深度
    acad.model.AddDimAligned(
        APoint(PIT_WIDTH + 1000, 0),
        APoint(PIT_WIDTH + 1000, -PIT_DEPTH),
        APoint(PIT_WIDTH + 1500, 0)
    ).TextOverride = f"开挖深度: {PIT_DEPTH/1000:.1f}m"
    
    # 墙体深度
    acad.model.AddDimAligned(
        APoint(PIT_WIDTH + 2000, 0),
        APoint(PIT_WIDTH + 2000, -WALL_DEPTH),
        APoint(PIT_WIDTH + 2500, 0)
    ).TextOverride = f"墙体深度: {WALL_DEPTH/1000:.1f}m"
    
    # 地下水位
    acad.model.AddText(
        f"地下水位: {WATER_LEVEL/1000:.1f}m",
        APoint(PIT_WIDTH/2, WATER_LEVEL - 500),
        300
    )

def draw_detailed_wall_section():
    """绘制地下连续墙细部剖面"""
    print("绘制地下连续墙细部剖面...")
    
    scale = 3  # 放大比例
    start_x = 5000
    start_y = -5000
    
    # 绘制墙体轮廓
    acad.model.AddLine(
        APoint(start_x, start_y),
        APoint(start_x + WALL_THICKNESS * scale, start_y)
    )
    acad.model.AddLine(
        APoint(start_x + WALL_THICKNESS * scale, start_y),
        APoint(start_x + WALL_THICKNESS * scale, start_y + 2000 * scale)
    )
    acad.model.AddLine(
        APoint(start_x + WALL_THICKNESS * scale, start_y + 2000 * scale),
        APoint(start_x, start_y + 2000 * scale)
    )
    acad.model.AddLine(
        APoint(start_x, start_y + 2000 * scale),
        APoint(start_x, start_y)
    )
    
    # 绘制钢筋网
    rebar_diameter = 25  # 钢筋直径
    rebar_spacing = 200  # 钢筋间距
    
    # 纵向钢筋
    for i in range(0, int(WALL_THICKNESS * scale), int(rebar_spacing * scale)):
        acad.model.AddCircle(
            APoint(start_x + i, start_y + 100 * scale),
            rebar_diameter * scale / 2
        )
    
    # 横向钢筋
    for j in range(0, 2000 * scale, int(rebar_spacing * scale)):
        for i in range(0, int(WALL_THICKNESS * scale), int(rebar_spacing * scale)):
            acad.model.AddCircle(
                APoint(start_x + i, start_y + j),
                rebar_diameter * scale / 2
            )
    
    # 添加标注
    acad.model.AddText(
        f"墙体厚度: {WALL_THICKNESS}mm",
        APoint(start_x + 100 * scale, start_y + 2100 * scale),
        200 * scale
    )
    
    acad.model.AddText(
        f"混凝土强度: {WALL_CONCRETE}",
        APoint(start_x + 100 * scale, start_y + 2000 * scale),
        200 * scale
    )
    
    acad.model.AddText(
        f"钢筋等级: {WALL_REBAR}",
        APoint(start_x + 100 * scale, start_y + 1900 * scale),
        200 * scale
    )

def draw_drainage_well_detail():
    """绘制降水井详图"""
    print("绘制降水井详图...")
    
    start_x = 10000
    start_y = -5000
    
    # 井管直径 400mm
    pipe_radius = 200
    well_radius = 400
    
    # 绘制井管
    acad.model.AddCircle(APoint(start_x, start_y), pipe_radius)
    
    # 绘制滤管外轮廓
    acad.model.AddCircle(APoint(start_x, start_y), well_radius)
    
    # 添加标注
    acad.model.AddText(
        f"井管直径: 400mm",
        APoint(start_x + 500, start_y),
        300
    )
    
    acad.model.AddText(
        f"井深: {WELL_DEPTH/1000:.1f}m",
        APoint(start_x + 500, start_y - 300),
        300
    )
    
    acad.model.AddText(
        f"降水井间距: {WELL_SPACING/1000:.0f}m",
        APoint(start_x + 500, start_y - 600),
        300
    )

def main():
    """主函数"""
    print("=" * 60)
    print("郑州市月影金沙小区基坑支护设计 CAD 绘图")
    print("=" * 60)
    
    # 清空当前图纸
    clear_drawing()
    
    # 绘制各视图
    draw_plan_view()  # 平面图
    draw_section_view()  # 剖面图
    draw_detailed_wall_section()  # 地下连续墙细部
    draw_drainage_well_detail()  # 降水井详图
    
    print("=" * 60)
    print("图纸绘制完成！")
    print("请在 AutoCAD 中查看绘制的基坑支护方案图纸")
    print("=" * 60)

if __name__ == "__main__":
    main()