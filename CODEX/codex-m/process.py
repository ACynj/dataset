import json


def load_entity_mapping(file_path):
    """加载实体映射（从entities.json），返回{实体ID: 实体label}的字典"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 提取每个实体的label，并用/替换空格
        mapping = {
            entity_id: info.get('label', entity_id).replace(' ', '/')
            for entity_id, info in data.items()
        }
        print(f"成功加载实体映射 {file_path}，共 {len(mapping)} 个实体")
        return mapping
    except FileNotFoundError:
        print(f"错误：实体文件 {file_path} 不存在")
        exit(1)
    except json.JSONDecodeError:
        print(f"错误：实体文件 {file_path} 格式不正确（非有效的JSON）")
        exit(1)
    except Exception as e:
        print(f"加载实体映射时出错：{str(e)}")
        exit(1)


def load_relation_mapping(file_path):
    """加载关系映射（从relations.json），返回{关系ID: 关系label}的字典"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # 提取每个关系的label，并用/替换空格
        mapping = {
            rel_id: info.get('label', rel_id).replace(' ', '/')
            for rel_id, info in data.items()
        }
        print(f"成功加载关系映射 {file_path}，共 {len(mapping)} 个关系")
        return mapping
    except FileNotFoundError:
        print(f"错误：关系文件 {file_path} 不存在")
        exit(1)
    except json.JSONDecodeError:
        print(f"错误：关系文件 {file_path} 格式不正确（非有效的JSON）")
        exit(1)
    except Exception as e:
        print(f"加载关系映射时出错：{str(e)}")
        exit(1)


def process_triples(input_file, output_file, entity_map, relation_map):
    """处理三元组文件，将实体ID和关系ID替换为真实名称（空格用/代替）"""
    processed = 0
    missing_entities = set()
    missing_relations = set()

    try:
        with open(input_file, 'r', encoding='utf-8') as in_f, \
                open(output_file, 'w', encoding='utf-8') as out_f:

            for line_num, line in enumerate(in_f, 1):
                line = line.strip()
                if not line:  # 跳过空行
                    continue
                # 分割三元组（假设用制表符分隔）
                parts = line.split('\t')
                if len(parts) != 3:
                    print(f"警告：三元组文件 {input_file} 第 {line_num} 行格式错误，已跳过：{line}")
                    continue

                head_id, rel_id, tail_id = parts

                # 映射头实体（处理空格）
                head_name = entity_map.get(head_id, head_id)
                if head_name == head_id:
                    missing_entities.add(head_id)
                # 确保即使是未找到映射的ID，其中的空格也会被替换
                head_name = head_name.replace(' ', '/')

                # 映射关系（处理空格）
                rel_name = relation_map.get(rel_id, rel_id)
                if rel_name == rel_id:
                    missing_relations.add(rel_id)
                rel_name = rel_name.replace(' ', '/')

                # 映射尾实体（处理空格）
                tail_name = entity_map.get(tail_id, tail_id)
                if tail_name == tail_id:
                    missing_entities.add(tail_id)
                tail_name = tail_name.replace(' ', '/')

                # 写入映射后的三元组（用制表符分隔）
                out_f.write(f"{head_name}\t{rel_name}\t{tail_name}\n")
                processed += 1

        print(f"处理完成 {input_file}，共处理 {processed} 条三元组")
        if missing_entities:
            print(f"  注意：有 {len(missing_entities)} 个实体未找到映射（示例：{list(missing_entities)[:5]}）")
        if missing_relations:
            print(f"  注意：有 {len(missing_relations)} 个关系未找到映射（示例：{list(missing_relations)[:5]}）")

    except FileNotFoundError:
        print(f"错误：三元组文件 {input_file} 不存在")
        exit(1)
    except Exception as e:
        print(f"处理 {input_file} 时出错：{str(e)}")
        exit(1)


def main():
    # 配置文件路径（请根据实际情况修改）
    entity_json_path = "./entities.json"  # 实体JSON文件路径
    relation_json_path = "./relations.json"  # 关系JSON文件路径
    triple_files = [  # 三元组文件（输入路径, 输出路径）
        ("./train.txt", "./train_mapped.txt"),
        ("./valid.txt", "./valid_mapped.txt"),
        ("./test.txt", "./test_mapped.txt")
    ]

    # 加载实体和关系映射（已处理空格）
    entity_map = load_entity_mapping(entity_json_path)
    relation_map = load_relation_mapping(relation_json_path)

    # 处理每个三元组文件（再次确保空格被替换）
    for input_path, output_path in triple_files:
        process_triples(input_path, output_path, entity_map, relation_map)

    print("\n所有文件处理完成！")


if __name__ == "__main__":
    main()