# Исходники диаграмм

Диаграммы вариантов использования, активностей, последовательностей и диаграмма паттерна CQRS описаны в PlantUML (`*.puml`). Диаграмма компонентов и ER-диаграммы строятся Python-скриптами (`*_gen.py`), которые формируют SVG; PNG получены из SVG для вставки в документы.

```
java -jar plantuml.jar -tpng design/uml/*.puml design/architecture/*.puml
cd design/uml && python3 component_gen.py   # -> component.svg
cd design/er && python3 concept_gen.py && python3 logical_gen.py   # -> concept.svg, logical.svg
```

Прототипы интерфейса (`prototypes/*.html`) – статические вайрфреймы, открываются в браузере.
