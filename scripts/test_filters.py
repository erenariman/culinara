import requests

base_url = "http://localhost:8000/api/v1/recipes"

def test_endpoint(params, description):
    print(f"\n--- Testing: {description} ---")
    print(f"Params: {params}")
    try:
        r = requests.get(base_url, params=params)
        if r.status_code == 200:
            data = r.json()
            print(f"Total Records: {data.get('total_records')} | Total Pages: {data.get('total_pages')} | Current Page: {data.get('current_page')} | Limit: {data.get('limit')}")
            print(f"Returned items count in this page: {len(data.get('data', []))}")
            if data.get('data'):
                for i, recipe in enumerate(data['data'][:3]): # print first 3
                    print(f"  - {recipe.get('title')} (Category: {recipe.get('category')}, Diet: {recipe.get('diet_type')}, Prep: {recipe.get('prep_time_minutes')}m)")
        else:
            print(f"Error {r.status_code}: {r.text}")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    test_endpoint({'limit': 2, 'page': 1}, "Basic Pagination (Page 1, Limit 2)")
    test_endpoint({'limit': 2, 'page': 2}, "Basic Pagination (Page 2, Limit 2)")
    test_endpoint({'category': 'Main Course'}, "Category Filter ('Main Course')")
    test_endpoint({'search': 'pie'}, "Search Filter ('pie')")
    test_endpoint({'sort_by': 'prep_time', 'order': 'asc'}, "Sorting by Prep Time ASC")
