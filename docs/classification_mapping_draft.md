# 分类映射草案 v0.1

本文件是待评审的规则，不是 95% 准确率证明。原始标签保留，不回写 OSM。

|规则|原始标签|标准类别|处理|
|---|---|---|---|
|C01|amenity=cafe|coffee_candidate|进入候选集；cafe 可能包含茶饮或其他饮品，需核实咖啡经营|
|O01|building=office|office_building|仅办公建筑层级，不累加楼内公司|
|B01|shop=mall 或 department_store|commercial_facility|商场/百货设施层级，节点与面须查重复|
|T01|railway=subway_entrance|subway_entrance|出入口层级，非车站/站台|
|X01|office=* 且没有以上核心标签|company_excluded|保留，不作为办公建筑计数|
|X02|同时命中多个核心类别|unknown_conflict|人工审查，未解决前不计数|

不纳入：泛 restaurant、fast_food、drink 商户；仅名称含“咖啡”的无标签对象；building=commercial（含其他商业用途）；landuse=commercial（区域层级）；building=retail（不等于商场）；railway=station、public_transport=platform、bus_stop。

示例：amenity=cafe + cuisine=tea 不自动确认咖啡店；building=office + office=company 是一个办公建筑记录；shop=mall 面内 shop=clothes 不纳入商业设施；地铁站 A 入口和 B 入口是两个真实入口，不能因同属一个站而合并。

## 几何和去重
点保留原坐标；闭合面与关系面采用面内代表点。开放 way 或无法重建关系面标记 geometry_missing。原始几何无效不自动修复并继续计数。
同类别、同名且 ≤30 m 或坐标重合只是重复候选；通过源对象、原始几何、标签与独立证据审核。地铁入口同名不能直接合并；同名品牌不同店不能直接合并；商场节点与面不得双计。跨来源去重不在本轮范围。

## 审核表与阈值
使用 evidence/classification_audit.csv：每类最多25条，总计最多100条，固定随机种子20261003；不足25全查。review_result 填 correct / incorrect / uncertain，附证据、日期、审核人，不能用同一规则自检当作人工正确率。
报告每类 correct、incorrect、uncertain、总数。保守正确率=correct/总数，不确定不计正确；每类样本至少20，且正确率≥95%才可通过类别门槛。总体平均不能掩盖某类失败。独立现实证据不足时只报告“标签语义映射一致性”，真实营业类别仍未验证。

待确认：cafe 中茶饮比例；办公建筑遗漏；百货节点与建筑面重复；关闭/停业标签；商场/百货是否需拆分；代表点对大型面边界的影响。建筑数量不能替代办公人口，商业设施数量不能替代经营热度。
