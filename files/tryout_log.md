# Tryouts

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
    - stored per line
    - embedding: OpenAIEmbeddings(request_timeout=60)
### Test Results
- Q1: What are the materials needed?
    - Aim: object retrieval form multiple db entry
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

'Nuts', 'Rice'
