# 02. 自訂函數、極座標幾何與圓柱繞流 (Functions & Polar Geometry)

## 1. 研究目的與問題背景

在水利工程、流體力學與結構周圍流場分析中，許多幾何對稱結構（如橋墩、圓形深開挖基坑、水下圓管）若以直角座標（$x, y$）描述邊界條件，方程式形式往往極其複雜。透過極座標變換（$r, \theta$），能大幅簡化軸對稱邊界問題。

本單元之研究目的為：
1. 掌握 Python 函式之引數預設值（Default Arguments）、關鍵字引數（Keyword Arguments）與區域變數作用域。
2. 運用 NumPy 之幾何運算模組（`hypot`、`arctan2`）精確計算向量長度與象限角度。
3. 實作流體力學經典理論——二維均勻流繞圓柱體之流線函數（Stream Function $\psi(r, \theta)$），實現幾何判定與流場數值計算。

---

## 2. 對應的原始 Python 程式碼

### 2.1 諧波自訂函式與參數預設值 (`Cell 4, 6`)
```python
def testfunc(x, A=1, theta=0):
    return A * np.cos(np.pi * x + theta)

print(testfunc(1))
print(testfunc(1, A=2))
print(testfunc(1, A=2, theta=np.pi / 4))
```

### 2.2 區域變數與線性函式 (`Cell 8, 10`)
```python
# 區域計算
def localtest(x):
    a, b = 3, 7
    return a * x + b
print(localtest(7))

# 參數傳入計算
def linear(x, a, b):
    return a * x + b
print(linear(5, 4, 6))
```

### 2.3 極座標角度與長度幾何計算 (`Cell 11, 12`)
```python
# 象限角度計算
x, y = -2, 2
theta = np.arctan2(y, x)
print(theta / np.pi)

# 圓半徑判斷
r = np.hypot(0.5, 0)
R = 1.5
print(r <= R)
```

### 2.4 二維圓柱繞流流線函數實作 (`Cell 13`)
```python
def psi(x, y, U=1, R=1):
    r = np.hypot(x, y)
    if r <= R:
        return 0.0
    theta = np.arctan2(y, x)
    return U * (r - R**2 / r) * np.sin(theta)

print(psi(2, 4, U=2, R=1.5))
print(psi(0.5, 0, U=2, R=1.5))
```

---

## 3. 重要函式與參數說明

- `testfunc(x, A=1, theta=0)`：
  - `A`：振幅（預設為 1）。
  - `theta`：初始相位角（預設為 0）。
  - 支援位置引數與關鍵字引數混合呼叫。
- `np.arctan2(y, x)`：全象限逆正切函式，依據 $(x, y)$ 正負號自動判定角度落入區間 $(-\pi, \pi]$，避免傳統 $\tan^{-1}(y/x)$ 因分母為零或象限混淆產生的數值錯誤。
- `np.hypot(x, y)`：歐幾里得距離運算 $\sqrt{x^2 + y^2}$，在數值上能避免平方相加時發生浮點數溢位（Overflow）或下溢（Underflow）。
- `psi(x, y, U=1, R=1)`：
  - `U`：遠場均勻流自由流速（Free-stream velocity）。
  - `R`：圓柱體半徑。
  - 當 $r \le R$ 時，該點落入實心圓柱體內部，流線值定義為邊界常數 $0.0$。

---

## 4. 相關數學公式及推導

### 4.1 諧波波形公式
$$f(x) = A \cos(\pi x + \theta)$$
- 當 $x = 1, A = 1, \theta = 0$ 時：
  $$f(1) = 1 \cdot \cos(\pi \cdot 1) = \cos(\pi) = -1.0$$
- 當 $x = 1, A = 2, \theta = 0$ 時：
  $$f(1) = 2 \cdot \cos(\pi) = -2.0$$
- 當 $x = 1, A = 2, \theta = \frac{\pi}{4}$ 時：
  $$f(1) = 2 \cdot \cos\left(\pi + \frac{\pi}{4}\right) = 2 \cdot \left(-\cos\frac{\pi}{4}\right) = 2 \cdot \left(-\frac{\sqrt{2}}{2}\right) = -\sqrt{2} \approx -1.41421356$$

### 4.2 直角座標至極座標之幾何轉換
給定二維點 $(x, y)$，其極座標表示法為：
$$r = \sqrt{x^2 + y^2}$$
$$\theta = \operatorname{atan2}(y, x) = \begin{cases} \arctan(y/x), & x > 0 \\ \arctan(y/x) + \pi, & x < 0, y \ge 0 \\ \arctan(y/x) - \pi, & x < 0, y < 0 \\ +\frac{\pi}{2}, & x = 0, y > 0 \\ -\frac{\pi}{2}, & x = 0, y < 0 \\ \text{undefined}, & x = 0, y = 0 \end{cases}$$
當 $(x, y) = (-2, 2)$ 時，位於第二象限（Quadrant II）：
$$\theta = \arctan(-1) + \pi = -\frac{\pi}{4} + \pi = \frac{3\pi}{4} \implies \frac{\theta}{\pi} = 0.75$$

### 4.3 理想流體繞圓柱體之流線函數推導
在流體力學位勢流（Potential Flow）理論中，不可壓縮、無旋流場之二維速度場可透過流線函數 $\psi$ 滿足拉普拉斯方程式：
$$\nabla^2 \psi = 0$$
在極座標系下，均勻平行流之流線函數為 $\psi_1 = U r \sin\theta$；偶極流（Doublet）之流線函數為 $\psi_2 = -\frac{\kappa}{2\pi} \frac{\sin\theta}{r}$。
兩者線性疊加，並令圓柱邊界 $r = R$ 處滿足不可穿透無滑移邊界條件（$\psi(R, \theta) = 0$），解得強度常數後，得到柱外流場（$r > R$）之流線函數：
$$\psi(r, \theta) = U \left( r - \frac{R^2}{r} \right) \sin\theta$$
流體在圓柱內（$r \le R$）不存在流動，規定 $\psi = 0$。

代入點 $(x, y) = (2, 4)$，參數 $U = 2, R = 1.5$：
$$r = \sqrt{2^2 + 4^2} = \sqrt{20} \approx 4.472136$$
$$\sin\theta = \frac{y}{r} = \frac{4}{\sqrt{20}}$$
$$\psi = 2 \times \left( \sqrt{20} - \frac{1.5^2}{\sqrt{20}} \right) \times \frac{4}{\sqrt{20}} = 2 \times \left( \sqrt{20} - \frac{2.25}{\sqrt{20}} \right) \times \frac{4}{\sqrt{20}}$$
$$= 2 \times \frac{20 - 2.25}{\sqrt{20}} \times \frac{4}{\sqrt{20}} = 2 \times \frac{17.75}{20} \times 4 = \frac{142}{20} = 7.1$$
理論值完全吻合程式輸出。

---

## 5. 實際執行結果

| 單元格 | 執行指令 | 終端機原始輸出 | 數學/物理意義驗證 |
| :---: | :--- | :--- | :--- |
| `Cell 6` | `testfunc(1)` | `-1.0` | $1 \times \cos(\pi) = -1$ |
| `Cell 6` | `testfunc(1, A=2)` | `-2.0` | $2 \times \cos(\pi) = -2$ |
| `Cell 6` | `testfunc(1, A=2, theta=np.pi/4)` | `-1.4142135623730954` | $2 \times \cos(5\pi/4) = -\sqrt{2}$ |
| `Cell 8` | `localtest(7)` | `28` | $3 \times 7 + 7 = 28$ |
| `Cell 10` | `linear(5, 4, 6)` | `26` | $4 \times 5 + 6 = 26$ |
| `Cell 11` | `print(theta/np.pi)` | `0.75` | 第二象限角 $3\pi/4 = 0.75\pi$ |
| `Cell 12` | `print(r<=R)` | `True` | $r=0.5 \le R=1.5$ 判定於柱內 |
| `Cell 13` | `psi(2, 4, U=2, R=1.5)` | `7.1000000000000005` | 柱外流場流線值理論推導 $7.1$ |
| `Cell 13` | `psi(0.5, 0, U=2, R=1.5)` | `0.0` | 柱體內部邊界屏蔽，嚴格歸零 |

---

## 6. 工程應用意義

1. **橋墩與深水基礎繞流沖刷分析**：橋樑圓形墩柱於河道中時，周圍水流速度場直接決定了墩柱側面的最大流速（理論最大流速在頂部與底部 $\theta = \pm \pi/2$ 處為 $2U$），這正是引發河床泥砂淘刷（Scour）與局部負壓空蝕的關鍵位置。
2. **海洋離岸風機單樁基礎（Monopile）波浪力學**：波浪通過圓形基樁時，利用位勢流流線與速度位（Velocity Potential），可透過莫里森方程式（Morison's Equation）推求波浪對基礎施加之慣性力。

---

## 7. 原始資料出處

- **來源檔案**：`RAW/W03/main.ipynb` (Cell 4–13) 與 `RAW/W03/main.py` (行 46–93)
- **原始標頭資訊**：參數、預設值、區域計算、極座標與流線實作
