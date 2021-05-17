# finetuning-RuGPT-for-poetry-generation
## **Генерация стиховторений на русском языке с помощью Сберовской ruGPT**

### **О работе**
Данная работа - дообучение модели ruGPT3 от Сбербанка для автоматической генерации стихотворений на русском языке.

В работе представлены два основных ноутбука:
1. "poetryWithoutStress.ipynb" - finetuning модели на датасете стихов без ударений
2. "poetryWithStress.ipynb" - finetuning модели на датасете стихов с ударениями

**TODO**: обучить больше эпох

### **Данные**
Два файла:
1. "poems.csv" - датасет стихотворений без ударений (~160тыс.)
2. "accentedPoems.csv" - датасет стихотворений с ударениями (~50тыс.)

Доступны по ссылке:
https://drive.google.com/file/d/1aeFdPbjDSvDP3cdVuqNAddhzTpnV-rna/view?usp=sharing

