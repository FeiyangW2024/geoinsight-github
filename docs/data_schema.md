# GeoInsight 数据 schema v0.1

状态：草案，未经正式任务数据冻结。日期：2026-10-03。

## 通用约定
JSON/JSONL UTF-8；ID 为字符串；经纬度为浮点度，顺序 longitude、latitude；距离米；时间 ISO 8601 UTC。所有必填字段不可省略，可空字段使用 null。unknown、未核验、缺失与 0 明确区分。数据署名：© OpenStreetMap contributors，ODbL-1.0，https://www.openstreetmap.org/copyright 。

## 数据集清单 dataset_manifest.json
|字段|类型/可空|含义|
|---|---|---|
|dataset_id|string|固定版本标识|
|source_url|string|实际原始下载 URL|
|source_timestamp|string/null|PBF header 中的源数据时间；null 时须说明|
|prepared_at|string|本次处理时间，不能冒充下载时间|
|license, license_url, attribution|string|数据许可及署名|
|source_crs|string|原始坐标系，OSM EPSG:4326|
|processing_version|string|处理/分类规则版本|
|freeze_status|string|raw_snapshot_only 或 evaluation_frozen；当前只冻结原始快照|
|files|object|各文件相对路径、bytes、sha256|
|md5_match|boolean/null|官方 MD5 比较结果，null 表示未验证|

正式冻结前增加 download_completed_at、coverage_geometry_file、coverage_boundary_timestamp、mapping_file_sha256、cleaned_data_sha256、candidate_file_sha256、task_protocol_sha256。任何一项变化产生新 dataset_id；不能沿用旧版本比较。

## POI：data/poi_draft.jsonl
|字段|类型/可空|含义|
|---|---|---|
|poi_id|string|源对象类型/ID，例 node/123；源对象 ID 不等于真实实体 ID|
|dataset_id|string|清单外键|
|source_object_type|string enum|node / way / relation|
|source_object_id|integer|OSM 对象 ID|
|name|string/null|原始名称，不能自动补造|
|raw_tags|object|完整原始标签|
|raw_geometry|GeoJSON Geometry/null|原始几何；缺失不能填合成坐标|
|source_crs|string|EPSG:4326|
|analysis_point|[number,number]/null|WGS84 经度、纬度；面内代表点|
|standard_category|string enum|coffee_candidate / office_building / commercial_facility / subway_entrance / unknown_conflict / company_excluded|
|mapping_rule_id|string|映射版本；正式版本需逐条规则 ID|
|geometry_method|string|native_point / point_on_surface|
|quality_flags|array<string>|geometry_missing / invalid_geometry / outside_expected_beijing_bbox 等|
|duplicate_group_id|string/null|实体重复组，当前人工审核前为 null|

coffee_candidate 不是已确认咖啡店。company_excluded 保留为质量证据，不参与办公建筑计数；unknown_conflict 不计数。正式 cleaned 数据须新增 review_status、evidence、reviewer、实体纳入/排除状态和理由；未经审核不能直接用 draft 数据发布业务结论。

## 候选点：evidence/probes.json
candidate_id:string；name:string；longitude/latitude:number；coordinate_source:string；stratum:string；use:string。当前 12 点为 synthetic WGS84 probe、phase0_only，不是门店地址，四种区域类型均为假设标签。正式任务点必须重新核实业务场景、坐标来源并冻结，不自动复用这些点。

Phase 0 检查附加字段：radius_1km_counts:object；nearest_subway_within_3km_m:number/null；extract_boundary_clearance_m:number/null；window_3km_inside_current_poly:boolean/null。最近入口缺失只表示冻结数据与搜索范围内未发现；不代表真实世界不存在。未出现类别不能直接解释为真实零密度。

## 正式指标结果（本轮仅定义，不生成产品接口）
result_id、candidate_id、dataset_id、rule_version、metric_name:string；value:number/null；unit:count/m；radius_m:number；status:valid/missing/insufficient_data；missing_reason:string/null；contributing_poi_ids:array<string>；computed_at:string。
五项 metric_name：coffee_count_1km、office_building_count_1km、commercial_facility_count_1km、subway_entrance_count_1km、nearest_subway_entrance_3km_m。
仅计纳入状态有效、几何有效且审核通过的实体。计数窗口 ≤1000 m，最近入口窗口 ≤3000 m，使用 WGS84 椭球测地距离，未四舍五入前判断边界。面按面内代表点计算，不作面积相交计数。最近入口不是步行距离。

## 人工与系统数据一致性契约
两条件加载完全相同的 cleaned_data_sha256、mapping_file_sha256、candidate_file_sha256；实验日志记录三者。人工查看器不得调用外部 POI 搜索或额外信息图层。底图仅作空间定位；若含额外商户信息应关闭。人工允许分类筛选、测距及表格公式，不提供预计算聚合统计。系统只自动化同样的数据处理与展示；数据获取/清洗投入另列。

Primary Metric 是完整任务耗时；任务质量是 guardrail。两者均不能通过更改 schema 中的数据范围或纳入规则来人为改善。
