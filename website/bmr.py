import math

def bmr(example, gender_col, age_col, weight_col, height_col, w_unit, h_unit):
    row_num, col_num = example.shape

    if col_num != 5:
        return False

    for i in range(row_num):
        try:
            height = float(example.iloc[i,height_col])
            weight = float(example.iloc[i,weight_col])
            age = int(example.iloc[i,age_col])
            gender = example.iloc[i,gender_col]
            bmr = float(example.iloc[i,4])
        except ValueError:
            # print("value error")
            return False

        if w_unit == "lb":
            weight *= 0.453592

        if h_unit == "in":
            height = height * 2.54

        if gender[0].lower() == 'f':
            calculate = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        elif gender[0].lower() == 'm':
            calculate = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)

        if not math.isclose(calculate, bmr , rel_tol = 0.01):
            # print(age,height,weight,gender)
            return False
        
    return True
