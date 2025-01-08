#!/usr/bin/env python3
import os
import time
import random
import sys
from math import sin, cos, pi

def clear():
    os.system('clear')

def create_firework():
    # 增加更多烟花字符
    chars = ['*', '✦', '✺', '✹', '✸', '✷', '★', '⭐️', '•', '∗', '＊', '✫', '✯', '✨', '⋆', '｡', '°']
    # 增加更多颜色
    colors = ['\033[91m', '\033[92m', '\033[93m', '\033[94m', '\033[95m', '\033[96m',
             '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m']
    return random.choice(colors) + random.choice(chars) + '\033[0m'

class Firework:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        # 随机起始位置
        self.x = random.randint(10, self.width-10)
        self.y = self.height - 1
        self.age = 0
        self.particles = []
        self.exploded = False
        self.trail = []

    def update(self):
        if not self.exploded:
            # 上升阶段
            self.trail.append((self.x, self.y))
            self.y -= 1
            if len(self.trail) > 5:  # 保持尾迹长度
                self.trail.pop(0)

            # 随机决定爆炸时机
            if self.y < random.randint(10, self.height-20):
                self.explode()
        else:
            # 爆炸后的粒子运动
            for p in self.particles:
                p['x'] += p['dx']
                p['y'] -= p['dy']
                p['dy'] -= 0.15  # 增加重力效果
                p['age'] += 1

            # 移除过期粒子
            self.particles = [p for p in self.particles if p['age'] < p['max_age']]
            self.age += 1

    def explode(self):
        self.exploded = True
        # 增加粒子数量，使用不同的图案
        num_particles = random.randint(20, 30)
        pattern = random.choice(['circle', 'spiral', 'double_spiral'])

        if pattern == 'circle':
            for angle in range(0, 360, int(360/num_particles)):
                rad = angle * pi / 180
                speed = random.uniform(0.8, 1.5)
                self.add_particle(rad, speed)
        elif pattern == 'spiral':
            for i in range(num_particles):
                rad = (i * 137.5 * pi / 180) % (2 * pi)
                speed = random.uniform(0.5, 2.0)
                self.add_particle(rad, speed)
        elif pattern == 'double_spiral':
            for i in range(num_particles):
                rad = (i * 137.5 * pi / 180) % (2 * pi)
                speed = random.uniform(0.5, 2.0)
                self.add_particle(rad, speed)
                self.add_particle(rad + pi, speed)

    def add_particle(self, rad, speed):
        self.particles.append({
            'x': self.x,
            'y': self.y,
            'dx': cos(rad) * speed,
            'dy': sin(rad) * speed,
            'char': create_firework(),
            'age': 0,
            'max_age': random.randint(20, 30)
        })

def draw_fireworks(width, height):
    # 创建多个烟花
    fireworks = [Firework(width, height) for _ in range(3)]
    screen = [[' ' for _ in range(width)] for _ in range(height)]

    while True:
        screen = [[' ' for _ in range(width)] for _ in range(height)]

        for fw in fireworks:
            # 绘制上升轨迹
            if not fw.exploded:
                for tx, ty in fw.trail:
                    if 0 <= int(tx) < width and 0 <= int(ty) < height:
                        screen[int(ty)][int(tx)] = '|'
                if 0 <= int(fw.x) < width and 0 <= int(fw.y) < height:
                    screen[int(fw.y)][int(fw.x)] = '↑'

            # 绘制爆炸粒子
            for p in fw.particles:
                x, y = int(p['x']), int(p['y'])
                if 0 <= x < width and 0 <= y < height:
                    screen[y][x] = p['char']

            fw.update()

            # 重置已经完成的烟花
            if fw.exploded and (len(fw.particles) == 0 or fw.age > 50):
                fw.reset()

        # 绘制画面
        clear()
        for row in screen:
            print(''.join(row))

        time.sleep(0.05)

def main():
    try:
        width, height = os.get_terminal_size()
        draw_fireworks(width, height)
    except KeyboardInterrupt:
        print("\n再见！")
        sys.exit(0)

if __name__ == "__main__":
    main()
