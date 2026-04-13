from __future__ import annotations

SITE_TITLE = "电磁场与电磁波长上下文知识库"
SOURCE_PDF = "电磁场与电磁波教学指导书_第4版_2006_清晰版.pdf"
SOURCE_NOTE = "扫描版教材，用作课程知识库编译的原始资料"

CHAPTERS = [
    {
        "slug": "01-fields-and-vectors",
        "title": "矢量场、坐标系与库仑定律",
        "chapter": "01",
        "tags": ["电场", "矢量分析", "库仑定律"],
        "summary": "建立电磁场问题的数学语言：位置矢量、梯度、散度、旋度，以及点电荷产生的静电场。这个页面是后续所有静态场分析的起点。",
        "highlights": [
            "电场强度描述单位正电荷在空间任一点所受的力。",
            "库仑定律给出点电荷之间的基本相互作用。",
            "用矢量分析工具可以把复杂分布的场统一写成积分表达。",
        ],
        "equations": [
            "F = qE",
            "E = (1 / (4\\pi\\epsilon_0)) * q / r^2 * r_hat",
            "nabla · E 与 nabla × E 是理解场结构的关键。",
        ],
        "related": ["02-gauss-law-and-flux", "03-potential-and-boundary-conditions"],
        "questions": [
            "为什么电场比电势更适合描述局部受力？",
            "点电荷和连续电荷分布的写法有什么区别？",
        ],
    },
    {
        "slug": "02-gauss-law-and-flux",
        "title": "高斯定律与电通量",
        "chapter": "02",
        "tags": ["高斯定律", "电通量", "静电场"],
        "summary": "把电场与包围电荷联系起来，借助对称性快速求解静电场。高斯定律是静电场最重要的积分关系之一。",
        "highlights": [
            "电通量刻画电场穿过闭合面的总效果。",
            "球对称、柱对称、平面对称问题往往适合高斯面法。",
            "高斯定律是麦克斯韦方程组的静态极限之一。",
        ],
        "equations": [
            "∮ E · dS = Q_enc / epsilon_0",
            "nabla · E = rho / epsilon_0",
        ],
        "related": ["01-fields-and-vectors", "03-potential-and-boundary-conditions", "07-maxwell-equations"],
        "questions": [
            "为什么高斯定律并不直接给出所有问题的电场？",
            "怎样判断一个问题是否适合选高斯面？",
        ],
    },
    {
        "slug": "03-potential-and-boundary-conditions",
        "title": "电势、边界条件与导体",
        "chapter": "03",
        "tags": ["电势", "边界条件", "导体"],
        "summary": "从标量电势出发，把静电问题转化为势函数求解问题，并总结导体、介质界面的边界条件。",
        "highlights": [
            "静电场是保守场，可以定义标量电势。",
            "导体内部静电平衡时电场为零，电荷分布在表面。",
            "边界条件把场量在不同介质界面上的连续/突变关系写清楚。",
        ],
        "equations": [
            "E = -nabla V",
            "nabla^2 V = -rho / epsilon_0",
            "切向电场连续，法向位移矢量满足跳变关系。",
        ],
        "related": ["02-gauss-law-and-flux", "04-conductors-dielectrics"],
        "questions": [
            "为什么电势更方便做数值求解？",
            "导体和介质边界上的连续条件如何记忆？",
        ],
    },
    {
        "slug": "04-conductors-dielectrics",
        "title": "导体、介质与极化",
        "chapter": "04",
        "tags": ["介质", "极化", "位移电流"],
        "summary": "把真实材料放进电磁场框架，理解极化、介电常数和位移矢量的物理意义。",
        "highlights": [
            "介质内部会发生偶极矩取向与极化，改变原有电场分布。",
            "位移矢量 D 将自由电荷和束缚电荷区分开来。",
            "材料参数决定静电场在不同介质中的传播与分布。",
        ],
        "equations": [
            "D = epsilon E",
            "nabla · D = rho_f",
            "P 与束缚电荷密度相关。",
        ],
        "related": ["03-potential-and-boundary-conditions", "07-maxwell-equations"],
        "questions": [
            "自由电荷与束缚电荷的区别是什么？",
            "为什么引入 D 能简化介质问题？",
        ],
    },
    {
        "slug": "05-static-magnetism",
        "title": "恒定磁场与安培定律",
        "chapter": "05",
        "tags": ["磁场", "安培定律", "毕奥-萨伐尔"],
        "summary": "从稳恒电流出发定义磁场，介绍毕奥-萨伐尔定律和安培环路定律，以及它们在对称结构中的应用。",
        "highlights": [
            "磁场来自运动电荷和电流。",
            "毕奥-萨伐尔定律适合逐段积分求磁场。",
            "安培环路定律在高对称问题中计算效率很高。",
        ],
        "equations": [
            "dB = (mu_0 / (4pi)) * I dl × r_hat / r^2",
            "∮ B · dl = mu_0 I_enc",
            "nabla × B = mu_0 J",
        ],
        "related": ["06-time-varying-fields", "07-maxwell-equations"],
        "questions": [
            "磁场为什么没有像电场那样的孤立磁荷？",
            "什么时候更适合用毕奥-萨伐尔，什么时候更适合用安培定律？",
        ],
    },
    {
        "slug": "06-time-varying-fields",
        "title": "时变电磁场与电磁感应",
        "chapter": "06",
        "tags": ["法拉第定律", "感应电动势", "位移电流"],
        "summary": "从变化的磁场和电场引出电磁感应，理解法拉第定律、楞次定律与位移电流的统一作用。",
        "highlights": [
            "变化的磁通会感生电场。",
            "位移电流让电流连续性在时变场中成立。",
            "这是从静态理论过渡到波动理论的关键章节。",
        ],
        "equations": [
            "∮ E · dl = -dPhi_B/dt",
            "nabla × E = -partial B / partial t",
            "J_d = partial D / partial t",
        ],
        "related": ["05-static-magnetism", "07-maxwell-equations", "08-plane-waves"],
        "questions": [
            "为什么变化的磁场会产生电场？",
            "位移电流的物理意义是什么？",
        ],
    },
    {
        "slug": "07-maxwell-equations",
        "title": "麦克斯韦方程组与统一图景",
        "chapter": "07",
        "tags": ["麦克斯韦方程", "统一理论", "电磁波"],
        "summary": "把静电、静磁和时变场统一到四条方程中，明确电磁场是一个相互耦合的整体。",
        "highlights": [
            "四条方程分别描述电荷源、磁场无源、感应关系和位移电流。",
            "它们是电磁波、传输线、波导分析的共同基础。",
            "从工程角度看，这一组方程是所有后续章节的母语。",
        ],
        "equations": [
            "nabla · D = rho_f",
            "nabla · B = 0",
            "nabla × E = -partial B / partial t",
            "nabla × H = J_f + partial D / partial t",
        ],
        "related": ["02-gauss-law-and-flux", "06-time-varying-fields", "08-plane-waves"],
        "questions": [
            "四条方程如何分别对应电场和磁场？",
            "为什么说麦克斯韦方程组统一了电与磁？",
        ],
    },
    {
        "slug": "08-plane-waves",
        "title": "均匀平面波与传播特性",
        "chapter": "08",
        "tags": ["平面波", "传播常数", "波阻抗"],
        "summary": "从麦克斯韦方程组推导电磁波方程，讨论均匀平面波在介质中的传播、衰减和极化。",
        "highlights": [
            "电场与磁场在传播方向上互相垂直。",
            "介质参数决定传播速度、衰减常数与波阻抗。",
            "波的极化是天线、通信和雷达中的核心指标。",
        ],
        "equations": [
            "d^2 E / dz^2 = mu epsilon d^2 E / dt^2",
            "v = 1 / sqrt(mu epsilon)",
            "E perp H perp 传播方向",
        ],
        "related": ["07-maxwell-equations", "09-waveguides-transmission-lines", "10-radiation-antennas"],
        "questions": [
            "波阻抗为什么会随介质变化？",
            "平面波的极化方式有哪些？",
        ],
    },
    {
        "slug": "09-waveguides-transmission-lines",
        "title": "传输线、驻波与波导",
        "chapter": "09",
        "tags": ["传输线", "驻波", "波导"],
        "summary": "把分布参数思想引入高频电路与导波结构，理解反射、驻波比和截止频率。",
        "highlights": [
            "传输线模型将电压、电流看成沿空间分布的量。",
            "阻抗失配会导致反射和驻波。",
            "波导结构决定模式、截止频率与能量传输方式。",
        ],
        "equations": [
            "partial V / partial x = -R I - L partial I / partial t",
            "partial I / partial x = -G V - C partial V / partial t",
            "gamma、Z0 和 VSWR 是典型工程指标。",
        ],
        "related": ["08-plane-waves", "10-radiation-antennas"],
        "questions": [
            "为什么高频下不能再把导线看成理想集中参数？",
            "驻波比过大说明什么问题？",
        ],
    },
    {
        "slug": "10-radiation-antennas",
        "title": "辐射、天线与远场",
        "chapter": "10",
        "tags": ["辐射", "天线", "远场"],
        "summary": "从时变电流和加速电荷出发，理解电磁辐射的形成机制，并把它和天线参数联系起来。",
        "highlights": [
            "只有时变源才能向远处辐射能量。",
            "远场区的场强与距离、方向和天线结构强相关。",
            "增益、方向图和极化是天线设计的核心指标。",
        ],
        "equations": [
            "辐射功率与加速电荷、时变电流相关。",
            "远场中场强通常近似按 1/r 衰减。",
        ],
        "related": ["08-plane-waves", "09-waveguides-transmission-lines"],
        "questions": [
            "近场和远场的本质区别是什么？",
            "为什么天线尺寸和工作频率有关？",
        ],
    },
]
