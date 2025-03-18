from GenAI import genai
from TextProcessing import processedtext
def generativedietplan(medicine_name,sideeffects,age,otherDiseases):
    prompt=f"""Generate a personalized diet plan to help manage the side effects of the given medicine. Consider the following details:

    Medicine Name: {medicine_name}
    Side Effects: {sideeffects}
    Age of the Patient: {age}
    other diseases: {otherDiseases}
    The diet plan should include food recommendations that can alleviate or minimize the side effects of the medicine. Also, suggest specific nutrients or ingredients that are beneficial for the patient's age and does not cause any effect patient with other diseases and overall well-being. 
    Make sure the diet is balanced, easily accessible, and practical for daily consumption.
    Include any lifestyle or dietary habits that could improve the patient’s overall health in relation to the side effects.
    make sure that it should not contain any index numbers instead of index number it should be determine with * symbol"""
    response=genai(prompt)
    print(response)
    result=processedtext(response)
    print(result)
    return result
