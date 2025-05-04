SELECT *
FROM `affable-curve-458422-n3.healthcare_analytics.insurance_claims`
LIMIT 10;
SELECT 
  smoker,
  ROUND(AVG(charges), 2) AS avg_medical_cost
FROM 
  `affable-curve-458422-n3.healthcare_analytics.insurance_claims`
GROUP BY 
  smoker;
SELECT 
  region,
  ROUND(AVG(charges), 2) AS avg_region_charges
FROM 
  `affable-curve-458422-n3.healthcare_analytics.insurance_claims`
GROUP BY 
  region
ORDER BY 
  avg_region_charges DESC;
SELECT 
  ROUND(BMI, 0) AS bmi_group,
  ROUND(AVG(charges), 2) AS avg_charges
FROM 
  `affable-curve-458422-n3.healthcare_analytics.insurance_claims`
GROUP BY 
  bmi_group
ORDER BY 
  bmi_group;
SELECT 
  sex,
  ROUND(AVG(charges), 2) AS avg_charges
FROM 
  `affable-curve-458422-n3.healthcare_analytics.insurance_claims`
GROUP BY 
  sex;
SELECT 
  children,
  COUNT(*) AS total_patients,
  ROUND(AVG(charges), 2) AS avg_charges
FROM 
  `affable-curve-458422-n3.healthcare_analytics.insurance_claims`
GROUP BY 
  children
ORDER BY 
  children;
