import streamlit as st
import requests


api_key = os.getenv('API_KEY')
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

def fetch_meals(diet, filters):
    params = {
        "apiKey": api_key,
        "diet": diet,
        "number": 5,
    }
    params.update(filters)
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print(f"Error: {response.status_code},{response.json().get('message')}")
        return []
    
def get_recipe_details(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {"apiKey": api_key,}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("sourceUrl", "NO LINK AVAILABLE")
    else:
        print(f"Error fetching recipe details: {response.status_code}")
        return "No link available"
    
       
def main():
    st.title("🍽️ Meal Suggestion App")
    st.write("Find meals based on your dietary preferences and nutrient requirements!")
    
    diet = st.selectbox("Select your dietary preference:", ["None", "Vegetarian", "Vegan"])
    
    filters = {}
    
    if st.checkbox("Specify nutrient filters"):
        min_calories = st.number_input("Minimum Calories", min_value=0, step=10)
        max_calories = st.number_input("Maximum Calories", min_value=0, step=10)
        if min_calories or max_calories:
            filters["minCalories"] = min_calories
            filters["maxCalories"] = max_calories

        min_protein = st.number_input("Minimum Protein (g)", min_value=0, step=1)
        max_protein = st.number_input("Maximum Protein (g)", min_value=0, step=1)
        if min_protein or max_protein:
            filters["minProtein"] = min_protein
            filters["maxProtein"] = max_protein

        min_fat = st.number_input("Minimum Fat (g)", min_value=0, step=1)
        max_fat = st.number_input("Maximum Fat (g)", min_value=0, step=1)
        if min_fat or max_fat:
            filters["minFat"] = min_fat
            filters["maxFat"] = max_fat
    
    if st.button("Get Meal Suggestions"):
        meals = fetch_meals(diet.lower(), filters)
        if meals:
            st.subheader("Here are some meal suggestions:")
            for meal in meals:
                recipe_url = get_recipe_details(meal["id"])
                st.markdown(f"**{meal['title']}**")
                st.markdown(f"[View Recipe]({recipe_url})")
                st.write("---")
        else:
            st.error("No meals found. Please try again.")

if __name__ == "__main__":
    main()
