- Confused result with multiple source, e.g.:
    ```
    USER: I would like to prepare a meal, including Kongbao chicken and Arabic Lentil soup, what should I prepare?

    BOT:
    USER: What are the materials needed? for Kongbao chicken and Arabic Lentil soup?
        USER: Make it a list in python

        BOT: (neglected chitchats)
            kongbao_chicken_materials = ['chicken', 'peanuts', 'vegetables', 'rice']
            arabic_lentil_soup_materials = ['olive oil', 'cumin seeds', 'mustard', 'curry leaves', 'onion', 'garlic cloves', 'spices (salt, cumin, cinnamon, turmeric, black pepper, curry)', 'yellow lentils', 'orange lentils']
    ```

- (given two files) There are only one file showed in the uploaded file list, though all hte data can be retrieved
    > Still solving

- Repaeted queried contents, e.g.:
    ```
    The kong bau chicken is a Chinese dish, ...

    The kong bau chicken is a Chinese dish, ...

    The kong bau chicken is a Chinese dish, ...
    ```
    > Multiple Indexing
    - cache indexing function
    > Multiple uploading file
    - use st.session_state['uploaded_list'] to store uploaded files


- Unrelated answer in the second conversation, e.g.:
    ```
    (given the receipt_for_kongbao.txt)
    USER: What are the ingredient of Kongbao Chicken?
    BOT: The ingredients are ...... (list the ingredient)
    USER: Make these a list in python
    BOT: There is nothing related to python in the quried data
    ```
    > Failed query in the second input corrupt the answer that should be related to conversation history
    - Give a prompt that make machine chose between history or query result, e.g.:
        ```
        The questions are all related to either query results or history

        If the question is related to querying results:
            - Extract information from queried result and answer the question
        Else if the question is related to history:
            - Extract information from history and answer the question
        If the question is not related to either querying result or history:
            - Politely inform that the result is not related to either history or database

        ```

- Query output duplication, e.g.:
    ```
    ['As with any stir-fry, you want to do all of your prep ahead of time because the cooking goes very quickly.',
    'As with any stir-fry, you want to do all of your prep ahead of time because the cooking goes very quickly.',
    'This Americanized version replaces those hard-to-find-ingredients with staples from your neighborhood supermarket.',
    'This Americanized version replaces those hard-to-find-ingredients with staples from your neighborhood supermarket.']
    ```
    > Duplicated upload to ElasticSearch DB when using stream
    - use st.cache and the db will store things only when new things are uploaded