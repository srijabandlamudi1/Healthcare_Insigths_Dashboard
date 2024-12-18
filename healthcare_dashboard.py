import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('cleaned_healthcare_dataset.csv')

# Data Preprocessing
data['date_of_admission'] = pd.to_datetime(data['date_of_admission'])
data['discharge_date'] = pd.to_datetime(data['discharge_date'])
data['stay_duration'] = (data['discharge_date'] - data['date_of_admission']).dt.days  # Length of stay in days

# Streamlit Layout
st.title("Healthcare Insights Dashboard")
st.write("""
This dashboard provides an in-depth analysis of patient demographics, billing patterns, admission types, and key medical insights.  
Use the sidebar filters to explore data based on **insurance providers, medical conditions, and gender**.  
The visualizations include univariate, bivariate, and multivariate analyses for a comprehensive understanding of the data.
""")

# Filters in the sidebar
st.sidebar.header("Select Filters")
insurance_provider_filter = st.sidebar.multiselect("Select Insurance Provider(s)", options=data['insurance_provider'].unique(), default=data['insurance_provider'].unique())
medical_condition_filter = st.sidebar.multiselect("Select Medical Condition(s)", options=data['medical_condition'].unique(), default=data['medical_condition'].unique())
gender_filter = st.sidebar.selectbox("Select Gender", options=["All", "male", "female"])


# Add Age Range Filter in the Sidebar
st.sidebar.header("Age Filter")
age_min, age_max = int(data['age'].min()), int(data['age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=age_min, max_value=age_max, value=(age_min, age_max))

# Start with the original data and apply all filters
filtered_data = data[
    (data['insurance_provider'].isin(insurance_provider_filter)) &
    (data['medical_condition'].isin(medical_condition_filter))
]

# Apply gender filter
if gender_filter != "All":
    filtered_data = filtered_data[filtered_data['gender'] == gender_filter]

# Apply age filter
filtered_data = filtered_data[(filtered_data['age'] >= age_range[0]) & (filtered_data['age'] <= age_range[1])]

# Apply filters to the data
# filtered_data = data[(data['insurance_provider'].isin(insurance_provider_filter)) & (data['medical_condition'].isin(medical_condition_filter))]
#if gender_filter != "All":
#    filtered_data = filtered_data[filtered_data['gender'] == gender_filter]

# Display number of patients after applying filters
st.subheader(f"Number of Patients: {len(filtered_data)}")

# **Univariate Analysis**

st.subheader("Univariate Analysis")

#1 Age Distribution
st.subheader("Age Distribution")
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(filtered_data['age'], kde=True, ax=ax, color='skyblue')
ax.set(title="Age Distribution", xlabel="Age", ylabel="Count")
st.pyplot(fig)
avg_age = filtered_data['age'].mean()
st.write(f"**Observation**: The average patient age is {avg_age:.0f} years. The age distribution is approximately uniform, with a fairly wide range of age groups.")

#2 Billing Amount Distribution
st.subheader("Billing Amount Distribution")
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(filtered_data['billing_amount'], kde=True, ax=ax, color='red')
ax.set(title="Billing Amount Distribution", xlabel="Billing Amount", ylabel="Count")
st.pyplot(fig)
st.write("**Observation**: The billing amount distribution shows a skew towards lower values, but a few high outliers exist.")

#3 Gender Distribution
st.subheader("Gender Distribution")
fig, ax = plt.subplots(figsize=(6, 4))
sns.countplot(x='gender', data=filtered_data, ax=ax, palette='Set1')
ax.set(title="Gender Distribution", xlabel="Gender", ylabel="Count")
st.pyplot(fig)
male_count = filtered_data['gender'].value_counts().get('male', 0)
female_count = filtered_data['gender'].value_counts().get('female', 0)
total_count = male_count + female_count
st.write(f"**Observation**: {male_count/total_count:.1%} of patients are male, while {female_count/total_count:.1%} are female. The dataset contains an almost equal distribution of male and female patients.")


#4 Blood Type Distribution
st.subheader("Blood Type Distribution")
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(x='blood_type', data=filtered_data, palette='Set2')
ax.set(title="Blood Type Distribution", xlabel="Blood Type", ylabel="Count")
st.pyplot(fig)
st.write("**Observation**: The Dataset contains an almost equal distribution of Blood Types.")

#5.Admission Type Distribution
st.subheader("Admission Type Distribution")
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(x='admission_type', data=filtered_data, palette='Set3')
ax.set(title="Admission Type Distribution", xlabel="Admission Type", ylabel="Count")
st.pyplot(fig)

#5.Insurance Provider Distribution
st.subheader("Insurance Provider Distribution")
fig, ax = plt.subplots(figsize=(6,4))
sns.countplot(x='insurance_provider', data=filtered_data, palette='coolwarm')
ax.set(title="Insurance Provider Distribution", xlabel="Insurance Provider", ylabel="Count")
st.pyplot(fig)

# **Bivariate Analysis**

st.subheader("Bivariate Analysis")

# 1.Age vs Admission Type
st.subheader("Age vs Admission Type")
fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(x='admission_type', y='age', data=filtered_data, ax=ax, palette='Set3')
ax.set(title="Age vs Admission Type", xlabel="Admission Type", ylabel="Age")
st.pyplot(fig)
st.write("**Observation**: Age distribution across admission types seems uniform with slight variations between types.")

# 2.Admission Type vs Insurance Provider
st.subheader("Admission Type vs Insurance Provider")
admission_insurance = data.groupby(['admission_type', 'insurance_provider']).size().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(admission_insurance, annot=True, fmt=".0f", cmap='YlGnBu', cbar=True)
ax.set(title="Admission Type vs Insurance Provider", xlabel="Admission Type", ylabel="Count")
st.pyplot(fig)
st.write("**Observation**: The distribution of admission types seems relatively balanced across different insurance providers.")


    # Observations
st.subheader("Observations for Bivariate Analysis")
st.write("1. The distribution of Age across different Admission Types reveals that the interquartile range (25th to 75th percentile) lies between ages 35 and 70, indicating that most patients fall within this age group for various admission types.")
st.write("2. The data shows a strong association between the Cigna insurance provider and the Urgent admission type, indicating that a significant proportion of urgent admissions are covered by Cigna.")
st.write("3. In contrast, there is a weaker association between the Aetna insurance provider and the Urgent admission type, suggesting that fewer urgent admissions are associated with Aetna.")


# **Multivariate Analysis**

st.subheader("Multivariate Analysis")

# 1. Billing Amount Across Insurance Providers and Admission Types
st.subheader("Billing Amount by Insurance Provider and Admission Type")
fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(x='insurance_provider', y='billing_amount', hue='admission_type', data=filtered_data, ax=ax)
ax.set(title="Billing Amount by Insurance Provider and Admission Type", xlabel="Insurance Provider", ylabel="Billing Amount")
plt.xticks(rotation=45)
st.pyplot(fig)
st.write("**Observation**: The Billing Amount shows slight variations based on the Admission Type for a given Insurance Provider, but these changes are not significant.")

# 2. Blood Type and Medical Conditions
st.subheader("Blood Type vs Medical Condition")
blood_condition = data.groupby(['blood_type', 'medical_condition']).size().unstack().fillna(0)
fig, ax = plt.subplots(figsize=(8, 4))
sns.heatmap(blood_condition, annot=True, fmt=".0f", cmap='YlGnBu')
ax.set(title="Blood Type vs Medical Condition", xlabel="Medical Conditions", ylabel="Blood Type")
st.pyplot(fig)
st.write("**Observation**: Blood types are fairly evenly distributed across different medical conditions.")

# 3. Length of Stay by Gender and Admission Type
st.subheader("Length of Stay by Gender and Admission Type")
fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(x='admission_type', y='stay_duration', hue='gender', data=filtered_data, ax=ax)
ax.set(title="Length of Stay by Gender and Admission Type", xlabel="Admission Type", ylabel="Length of Stay (Days)")
st.pyplot(fig)
st.write("**Observation**: There are small gender-based differences in length of stay across different admission types.")

# 4. Correlation Between Age, Billing Amount, and Medications
st.subheader("Age vs Billing Amount Colored by Admission Type")

fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='age', y='billing_amount', hue='admission_type', data=data, palette='Set2', s=100, alpha=0.7, ax=ax)
plt.title("Age vs Billing Amount Colored by Admission Type")
plt.xlabel("Age")
plt.ylabel("Billing Amount")
st.pyplot(fig)


st.subheader("Final Insights and Observations")

st.write("""
### **Univariate Analysis**
1. **Age Distribution**: The age distribution is uniformly spread between **13 to 89 years**, with an average age of approximately **52 years**.
2. **Billing Amount Distribution**: Most billing amounts fall below **40,000**, with a few high outliers exceeding **50,000**.
3. **Gender Distribution**: Gender representation is perfectly balanced at **50% male** and **50% female**.
4. **Blood Type Distribution**: All blood types are evenly distributed across patients.
5. **Admission Type Distribution**: Urgent, Emergency, and Elective admissions show **equal representation**, with Urgent admissions being slightly higher.
6. **Insurance Provider Distribution**: Major providers (**Cigna, Aetna, UnitedHealthcare, Medicare, and Blue Cross**) have **equal distribution**.

### **Bivariate Analysis**
7. **Age vs Admission Type**: Age distributions are consistent across admission types. Elective admissions show a **slightly older age group** on average.
8. **Admission Type vs Insurance Provider**: 
   - **Cigna** has the **highest association** with Urgent admissions.
   - Aetna has fewer Urgent admissions, indicating a weaker association.

### **Multivariate Analysis**
9. **Billing Amount by Insurance Provider and Admission Type**: 
   - Billing amounts remain consistent across admission types for all insurance providers.
10. **Blood Type vs Medical Condition**: Blood types are evenly distributed across medical conditions with **no significant associations**.
11. **Length of Stay by Gender and Admission Type**:
     - Male patients have slightly **longer stays** for Emergency admissions.
12. **Age vs Billing Amount Colored by Admission Type**: 
     - No strong correlation exists between **age** and **billing amounts**, regardless of admission type.

### **Key Takeaways**
- The dataset shows a **balanced representation** across demographics (age, gender, blood type) and insurance providers.
- Billing amounts cluster below **40,000**, with occasional high outliers.
- **Cigna** strongly correlates with Urgent admissions, while other providers remain balanced.
- No significant relationships exist between blood type, medical conditions, or billing trends with age.

These insights can assist healthcare providers in understanding patient demographics, optimizing resources, and identifying trends in admission types and billing patterns.
""")