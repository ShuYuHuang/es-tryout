# Tryouts

## 6.Oct.2023
### Params
- prompt:
    ```
    Queried results form database:
    {queried}

    History:
    {history}

    You are asked:
    {input}

    The questions are all related to either query results or history

    If the question is related to querying results:
    - Extract information from queried result and answer the question
    Else if the question is related to history:
    - Extract information from history and answer the question
    If the question is not related to either querying result or history:
    - Politely inform that the result is not related to either history or database
    ```
- data: 
    - receipe_for_kongbao.txt
        - partially ordered SOP with materials and actions
        - spec: 18 lines, 60~300 words per line
    - receipe_arabic_lentil_soup.txt
        - partially ordered SOP with materials and actions
        - spec: 10 lines, 23~240 words per line
- vector db: ElasticsearchStore.from_documents
    - args: distance_strategy="COSINE"
    - embedding: OpenAIEmbeddings(request_timeout=60)
### Test Results
- CTRL: Answering form 1 file source in single reply:
    - splitter args: chunk_size=100, chunk_overlap=0
    - elasticsearch args: k=5
    - Conversation for receipe_for_kongbao.txt:
        ```
        USER: What are the materials needed?
        USER: Make it a list in python
        BOT:
            materials_needed = [
                "Bell pepper",
                "Celery",
                "Scallions",
                "Garlic",
                "Balsamic vinegar",
                "Soy sauce",
                "Hoisin sauce",
                "Sesame oil",
                "Sugar",
                "Cornstarch",
                "Red pepper flakes",
                "Ground ginger",
                "Water"
            ]
        ```
        - Queried results:
            ```
            As with any stir-fry, you want to do all of your prep ahead of time because the cooking goes very quickly.
            This Americanized version replaces those hard-to-find-ingredients with staples from your neighborhood supermarket.
            3. Meanwhile, chop the bell pepper, celery, scallions, and garlic.
            4. In another medium bowl, prepare the sauce by whisking together all of the sauce ingredients: balsamic vinegar, soy sauce, hoisin sauce, sesame oil, sugar, cornstarch, red pepper flakes, ground ginger, and water.
            Since the chicken needs to marinate for 15 minutes, get that started first.
            ```
    - Conversation for receipe_arabic_lentil_soup.txt:
        ```
        USER: What are the materials needed?
        USER: Make it a list in python
        BOT:
            materials_needed = [
                "Lentils (yellow and orange)",
                "Cream",
                "Cheddar cheese",
                "Vegetables (potatoes, carrots, pumpkin, tomatoes, red bell pepper)",
                "Boiling water or chicken broth",
                "Lemon juice"
            ]
        ```
        - Queried result:
            ```
            4. Then we add two kinds of lentils, yellow and orange
            5. Get excited together
            8. Then add a little cream and a piece of cheddar cheese
            9. Then we grind vegetables and lentils
            3. Add (potatoes + carrots + pumpkin + tomatoes + red bell pepper)
            6. Then we put boiling water .. or chicken broth ..
            7. Leave until leveling
            10. Finally, a little lemon juice
            ```
- EXP: Answering from two file sources in single reply:
    - splitter args: chunk_size=100, chunk_overlap=0
    - elasticsearch args: k=5
    - Conversation:
        ```
        USER: What are the materials needed? for Kongbao chicken and Arabic Lentil soup?
        USER: Make it a list in python

        BOT: (neglected chitchats)
            kongbao_chicken_materials = ['chicken', 'peanuts', 'vegetables', 'rice']
            arabic_lentil_soup_materials = ['olive oil', 'cumin seeds', 'mustard', 'curry leaves', 'onion', 'garlic cloves', 'spices (salt, cumin, cinnamon, turmeric, black pepper, curry)', 'yellow lentils', 'orange lentils']
        ```
    - Query results:
        ```
        2. Ingredients and method for making lentil soup arabic : In a little olive oil, sauté: Cumin seeds + mustard + curry leaves. A chopped onion. Than the garlic cloves. A pinch of spices (salt, cumin, cinnamon, turmeric, black pepper, curry)
        how to make lentil soup arabic recipe in english at home
        1. Lentil soup with vegetables
        4. Then we add two kinds of lentils, yellow and orange
        5. Get excited together
        Kung pao chicken is a popular Chinese restaurant dish of stir-fried chicken, peanuts and vegetables.
        It has all the same spicy, sweet, and sour appeal of traditional kung pao chicken, and it makes a really nice weeknight dinner with a side of rice.
        ```
        - Mixing of results from both source
        - Not enought top_k amout for 2 sources
- Conclusion of tryout
    > Query from multiple sources needs more top_k amout, and it causes information coupling
    - Solution 1: Multi-layer DB
        - 1st layer: indices for files
        - 2nd layer: indices for word chunks in files
        ```
        Provide more accurate file source
        Cannot resolve the multi-source query demand
        ```
    - Solution 2: Multi-layer QA:
        - 1st QA: Organize separate queries needed
        - n'th QA: Query for each sub-problem
        ```
        Provide accurate file source while resolve the multi-source demand
        Cost more tokens and takes more time 
        ```
---
## 4.Oct.2023
### Params
- prompt:
    ```
    You are given the following history:
    {history}

    and the queried results:
    {queried}

    You are asked:
    {input}

    Please answer carefully with the information given by queried result and history
    ```
- chain: LLMChain
- data: receipe_for_kongbao.txt
    - partially ordered SOP with materials and actions
    - spec: 18 lines, 60~300 words per line
- vector db: ElasticsearchStore.from_documents
    - args: distance_strategy="COSINE"
    - embedding: OpenAIEmbeddings(request_timeout=60)
### Test Results
- object retrieval form multiple db entry
    - Prompt: What are the materials needed?
    - splitter args: chunk_size=500, chunk_overlap=0
        - Result:
            ```
            ['Chicken', 'Soy sauce', 'Dry sherry', 'Cornstarch', 'Bell pepper', 'Celery', 'Scallions', 'Garlic', 'Balsamic vinegar', 'Hoisin sauce', 'Sesame oil', 'Sugar', 'Red pepper flakes', 'Ground ginger', 'Water', 'Nuts', 'Rice']
            ```
            - non repeated
            - missing: salt (though included in the query)
        - Query result: whole paragraph
        - Introspection: though get a good result, the paragraph is too large
    - splitter args: chunk_size=100, chunk_overlap=0
        - Result:
            ```
            Based on the queried results, the materials needed for the recipe are not provided. The queried results only mention the cooking process and the substitution of ingredients, but they do not mention the specific materials required for the recipe. Therefore, we cannot determine the materials needed based on the given information.
            ```
            - cannot find content
        - Query result:
            ```
            ['As with any stir-fry, you want to do all of your prep ahead of time because the cooking goes very quickly.',
            'As with any stir-fry, you want to do all of your prep ahead of time because the cooking goes very quickly.',
            'This Americanized version replaces those hard-to-find-ingredients with staples from your neighborhood supermarket.',
            'This Americanized version replaces those hard-to-find-ingredients with staples from your neighborhood supermarket.']
            ```
        - Introspection: small chunk size might not include the contents needed
    - splitter args: chunk_size=200, chunk_overlap=0
        - Result:
            ```
            ['Balsamic vinegar', 'Soy sauce', 'Hoisin sauce', 'Sesame oil', 'Sugar', 'Cornstarch', 'Red pepper flakes', 'Ground ginger', 'Water']
            ```
            - non repeated
            - missing: 'Chicken', 'Dry sherry', 'Cornstarch', 'Bell pepper', 'Celery', 'Scallions', 'Garlic', 'Nuts', 'Rice', 'Salt'
        - Query result:
            ```
            ['This Americanized version replaces those hard-to-find-ingredients with staples from your neighborhood supermarket.',
            'This Americanized version replaces those hard-to-find-ingredients with staples from your neighborhood supermarket.',
            '4. In another medium bowl, prepare the sauce by whisking together all of the sauce ingredients: balsamic vinegar, soy sauce, hoisin sauce, sesame oil, sugar, cornstarch, red pepper flakes, ground ginger, and water.',
            '4. In another medium bowl, prepare the sauce by whisking together all of the sauce ingredients: balsamic vinegar, soy sauce, hoisin sauce, sesame oil, sugar, cornstarch, red pepper flakes, ground ginger, and water.']
            ```
        - Introspection: bad for searching if some contents are not included in single chunk
    - splitter args: chunk_size=300, chunk_overlap=100
        - Result:
            ```
            ['Bell pepper', 'Celery', 'Scallions', 'Garlic', 'Balsamic vinegar', 'Soy sauce', 'Hoisin sauce', 'Sesame oil', 'Sugar', 'Cornstarch', 'Red pepper flakes', 'Ground ginger', 'Water', 'Nuts', 'Rice']
            ```
            - non repeated
            - missing: 'Chicken', 'Dry sherry', 'Salt'
        - Query result:
            ```
            ['13. Stir in the nuts. Taste and adjust seasoning, if necessary, and serve with rice.',
            '13. Stir in the nuts. Taste and adjust seasoning, if necessary, and serve with rice.',
            '13. Stir in the nuts. Taste and adjust seasoning, if necessary, and serve with rice.',
            '11. Add the reserved vegetables and reserved chicken to the pan, along with the sauce.\n\n12. Reduce the heat to low. Cook until the chicken and vegetables are warmed through and the sauce is thickened, about 30 seconds.']
            ```
        - Introspection: higher chunk size with overlab will increase the coverage
    - splitter args: chunk_size=400, chunk_overlap=100
        - Result:
            ```
            ['Bell pepper', 'Celery', 'Scallions', 'Garlic', 'Balsamic vinegar', 'Soy sauce', 'Hoisin sauce', 'Sesame oil', 'Sugar', 'Cornstarch', 'Red pepper flakes', 'Ground ginger', 'Water', 'Nuts', 'Rice']
            ```
            - non repeated
            - missing: 'Chicken', 'Dry sherry', 'Salt'
        - Query result:
            ```
            ['13. Stir in the nuts. Taste and adjust seasoning, if necessary, and serve with rice.',
            '13. Stir in the nuts. Taste and adjust seasoning, if necessary, and serve with rice.',
            '13. Stir in the nuts. Taste and adjust seasoning, if necessary, and serve with rice.',
            '11. Add the reserved vegetables and reserved chicken to the pan, along with the sauce.\n\n12. Reduce the heat to low. Cook until the chicken and vegetables are warmed through and the sauce is thickened, about 30 seconds.']
            ```
        - Introspection: higher chunk size with overlab will increase the coverage
