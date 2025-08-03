import random
import streamlit as st
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
import numpy as np
import time
import pandas as pd


subjects = [
    {"name": "رياضيات 1", "level": 1},
    {"name": "الميكانيك الهندسي", "level": 1},
    {"name": "مدخل إلى البرمجة", "level": 1},
    {"name": " الرياضيات 2", "level": 1},
    {"name": "الجودة والوثوقية", "level": 1},
    {"name": "أسس الهندسة الكهربائية", "level": 1},
    {"name": "كيمياء", "level": 1},

    {"name": "رياضيات 3", "level": 2},
    {"name": "فيزياء ", "level": 2},
    {"name": "الرسم الهندسي", "level": 2},
    {"name": "رياضيات متقطعة", "level": 2},
    {"name": "تطبيقات في الاحصاء الهندسي ", "level": 2},
    {"name": "تحليل عددي", "level": 2},
    {"name": "دارات منطقية ", "level": 2},
    {"name": "مدخل الى علوم الحاسوب ", "level": 2},
    {"name": "مدخل الى الخوارزميات", "level": 2},
    {"name": "مقدمة في تقانة الشبكات", "level": 2},

    {"name": "الخوارزميات وبنى المعطيات", "level": 3},
    {"name": "البرمجة غرضية التوجه", "level": 3},
    {"name": "لغة التجميع", "level": 3},
    {"name": "مدخل الى الذكاء الصنعي", "level": 3},
    {"name": "قواعد معطيات 1", "level": 3},
    {"name": "تقانة الانترنت وبرمجة الويب", "level": 3},
    {"name": "تنظيم وبنيان الحواسيب", "level": 3},
    {"name": "تراسل 1", "level": 3},
    {"name": "برمجة النظم", "level": 3},
    {"name": "قواعد البيانات", "level": 3},
    {"name": "نمذجة ومحاكاة", "level": 3},
    {"name": " مهارات اللغة الانكليزية", "level": 3},

    {"name": "بحوث العمليات", "level": 4},
    {"name": "هندسة البرمجيات 1", "level": 4},
    {"name": "قواعد المعطيات 2", "level": 4},
    {"name": "نظم تشغيل", "level": 4},
    {"name": "نظرية الحوسبة", "level": 4},
    {"name": "امن نظم المعلومات", "level": 4},
    {"name": "تراسل 2", "level": 4},
    {"name": "تصميم المترجمات", "level": 4},
    {"name": "تطوير التطبيقات", "level": 4},

    {"name": "نظم موزعة", "level": 5, "departments": ["برمجيات", "شبكات", "ذكاء"]},
    {"name": "نظم ادارية", "level": 5, "departments": ["برمجيات", "شبكات", "ذكاء"]},
    {"name": "انظمة الوسائط", "level": 5, "departments": ["برمجيات", "شبكات", "ذكاء"]},
    {"name": "برمجة تفرعية", "level": 5, "departments": ["برمجيات", "شبكات", "ذكاء"]},

    {"name": "نظم استرجاع البيانات", "level": 5, "departments": ["برمجيات", "ذكاء"]},
    {"name": "الرجل الالي", "level": 5, "departments": ["ذكاء"]},
    {"name": "الرؤية الحاسوبية", "level": 5, "departments": ["ذكاء"]},
    {"name": "النمذجة والمحاكاة", "level": 5, "departments": ["ذكاء"]},
    {"name": "التعلم الالي", "level": 5, "departments": ["ذكاء"]},

    {"name": "هندسة برمجيات2", "level": 5, "departments": ["برمجيات"]},
    {"name": "قواعد معطيات متقدمة", "level": 5, "departments": ["برمجيات"]},
    {"name": "بناء المترجمات", "level": 5, "departments": ["برمجيات"]},
    {"name": "الحوسبة النقالة", "level": 5, "departments": ["برمجيات", "شبكات"]},

    {"name": "الشبكات اللاسلكية", "level": 5, "departments": ["شبكات"]},
    {"name": "امن شبكات حاسوبية", "level": 5, "departments": ["شبكات"]},
    {"name": "ادارة الشبكات", "level": 5, "departments": ["شبكات"]},
    {"name": "تصميم الشبكات", "level": 5, "departments": ["شبكات"]},

]

NUM_SUBJECTS = len(subjects)
exam_days = list(range(7))
exam_slots = ["8AM", "10AM", "12PM"]
exam_periods = [(d, t) for d in exam_days for t in exam_slots]

# إعدادات الجينات
if "FitnessMin" not in creator.__dict__:
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
if "Individual" not in creator.__dict__:
    creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("gene", lambda: random.randint(0, len(exam_periods) - 1))
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.gene, n=NUM_SUBJECTS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
def fitness(individual):
    penalty = 0
    schedule = {}
    exams_by_day = {}
    subject_by_day = {}
    departments_by_day = {}

    for idx, period_index in enumerate(individual):
        subject = subjects[idx]
        level = subject["level"]
        day, slot = exam_periods[period_index]
        period = (day, slot)

        # حفظ الجدولة حسب الفترة
        schedule.setdefault(period, []).append((idx, level))

        # حفظ الامتحانات حسب اليوم
        exams_by_day.setdefault(day, []).append((slot, level, idx))

        # حفظ المستويات حسب اليوم
        subject_by_day.setdefault(day, []).append((level, idx))

        # حفظ الأقسام حسب اليوم
        if "departments" in subject:
            for dept in subject["departments"]:
                departments_by_day.setdefault(day, {}).setdefault(dept, []).append(subject["name"])

    # 1️⃣ عقوبة: مواد عامة في نفس الفترة (فرق مستوى <= 1)
    for exams in schedule.values():
        for i in range(len(exams)):
            idx1, lvl1 = exams[i]
            subj1 = subjects[idx1]
            if "departments" in subj1 and len(subj1["departments"]) <= 2:
                continue
            for j in range(i + 1, len(exams)):
                idx2, lvl2 = exams[j]
                subj2 = subjects[idx2]
                if "departments" in subj2 and len(subj2["departments"]) <= 2:
                    continue
                if abs(lvl1 - lvl2) <= 1:
                    penalty += 30

    # 2️⃣ عقوبة: مادتان بنفس المستوى في نفس اليوم على فترات متتالية (فقط العامة)
    for exams in exams_by_day.values():
        exams.sort()
        for i in range(len(exams) - 1):
            time1, lvl1, idx1 = exams[i]
            time2, lvl2, idx2 = exams[i + 1]
            subj1 = subjects[idx1]
            subj2 = subjects[idx2]
            if ("departments" in subj1 and len(subj1["departments"]) <= 2) or ("departments" in subj2 and len(subj2["departments"]) <= 2):
                continue
            if lvl1 == lvl2:
                penalty += 15

    # 3️⃣ عقوبة: أكثر من مادتين بنفس المستوى في نفس اليوم (فقط العامة)
    for levels in subject_by_day.values():
        level_counts = {}
        for lvl, idx in levels:
            subj = subjects[idx]
            if "departments" in subj and len(subj["departments"]) <= 2:
                continue
            level_counts[lvl] = level_counts.get(lvl, 0) + 1
        for count in level_counts.values():
            if count > 2:
                penalty += (count - 2) * 30

    # 4️⃣ عقوبة: تداخل تخصصات داخل نفس الفترة
    for exams in schedule.values():
        departments_in_period = []
        for idx, _ in exams:
            subj = subjects[idx]
            if "departments" in subj:
                departments_in_period.append(set(subj["departments"]))
        for i in range(len(departments_in_period)):
            for j in range(i + 1, len(departments_in_period)):
                intersection = departments_in_period[i] & departments_in_period[j]
                if intersection:
                    penalty += 30 * len(intersection)

    # 5️⃣ عقوبة: أكثر من مادة من نفس التخصص في نفس اليوم (يشمل المواد المشتركة بشكل دقيق)
    for day, dept_subjects in departments_by_day.items():
        for dept, subject_list in dept_subjects.items():
            subject_counts = {}
            for subj in subject_list:
                subject_counts[subj] = subject_counts.get(subj, 0) + 1
            for count in subject_counts.values():
                if count > 1:
                    penalty += (count - 1) * 30


    return (penalty,)

toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=len(exam_periods) - 1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

def run_ga_with_logging():
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    logbook = tools.Logbook()
    logbook.header = ["gen", "avg", "min", "max"]
    
    for gen in range(100):
        offspring = algorithms.varAnd(pop, toolbox, cxpb=0.7, mutpb=0.3)
        fits = list(map(toolbox.evaluate, offspring))
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        pop[:] = toolbox.select(offspring, k=len(pop))
        record = stats.compile(pop)
        logbook.record(gen=gen, **record)
        
    hof.update(pop)
    return hof[0], logbook

# واجهة Streamlit
st.set_page_config(page_title="منظّم الجدول الامتحاني", layout="wide")
st.title("📅 مولد الجدول الامتحاني باستخدام الخوارزميات الجينية")

st.markdown("""
🔍 **الوصف:** هذا البرنامج يقوم بتوزيع المواد الامتحانية بطريقة ذكية بحيث تتباعد المواد ذات المستويات المتقاربة والصعبة على الأيام والأوقات المختلفة.
""")



if st.button("🔁 توليد جدول امتحاني"):
    start_time = time.time()  # ⏱️ بداية القياس
    best, log = run_ga_with_logging()
    end_time = time.time()  # ⏱️ نهاية القياس
    execution_time = end_time - start_time

    # تحضير الجدول الفارغ
    table_data = {slot: [""] * len(exam_days) for slot in exam_slots}

    # ملء البيانات حسب كل مادة
    for idx, period_index in enumerate(best):
        subject = subjects[idx]
        day, slot = exam_periods[period_index]
        info = f"{subject['name']} (المستوى {subject['level']})"
        if table_data[slot][day]:
            table_data[slot][day] += "\n" + info  # فاصل سطر
        else:
            table_data[slot][day] = info

    # تحويل الجدول إلى DataFrame مع تسمية الصفوف (الأيام)
    df = pd.DataFrame(table_data, index=[f"اليوم {i+1}" for i in range(len(exam_days))])

    st.success("✅ تم توليد الجدول الامتحاني بنجاح")
    st.info(f"🕒 زمن تنفيذ الخوارزمية: {execution_time:.2f} ثانية")

    # عرض الجدول مع التفاف النص داخل الخلايا
    st.dataframe(
        df.style.set_properties(**{'white-space': 'pre-wrap'}),
        use_container_width=True
    )
    st.subheader("📈 تقييم أداء الخوارزمية عبر الأجيال")
    generations = log.select("gen")
    min_fitness = log.select("min")
    avg_fitness = log.select("avg")
    max_fitness = log.select("max")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(generations, min_fitness, label="Best Fitness", color="green")
    ax.plot(generations, avg_fitness, label="Meduime Fitness", color="blue")
    ax.plot(generations, max_fitness, label="Worst Fitness", color="red")
    ax.set_xlabel("Number of generations")
    ax.set_ylabel("Penalty value (Fitness)")
    ax.set_title("Genetic Algorithm Evaluation")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

if st.checkbox("📋 عرض تفاصيل العقوبات"):
    st.markdown("""
    - 1️⃣ مواد عامة في نفس الفترة بمستويات متقاربة: `30 نقطة`
    - 2️⃣ مادتان من نفس المستوى في نفس اليوم على فترات متتالية: `15 نقطة`
    - 3️⃣ أكثر من مادتين من نفس المستوى في نفس اليوم: `30 نقطة لكل مادة إضافية`
    - 4️⃣ تداخل تخصصات داخل نفس الفترة: `30 نقطة لكل تداخل`
    - 5️⃣ أكثر من مادة من نفس التخصص في نفس اليوم: `30 نقطة لكل مادة إضافية`
    """)

# streamlit run exam_scheduler_app.py