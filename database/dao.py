from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def get_category():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
         SELECT DISTINCT category_name, id
         FROM category
         ORDER BY category_name 
         """
        cursor.execute(query)

        for row in cursor:
            result.append((row["category_name"], row["id"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_date_range():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT order_date
                    FROM `order` 
                    ORDER BY order_date """
        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    def get_product(category):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
         SELECT DISTINCT p.id, p.product_name
         FROM product p
         JOIN category c ON p.category_id = c.id
         WHERE c.category_name = %s 
         ORDER BY product_name 
         """

        cursor.execute(query, (category,))
        for row in cursor:
            result.append((row["product_name"], row["id"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_product_in_category(category, first, last):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
         SELECT DISTINCT p.id, p.product_name, COUNT(DISTINCT o1.id) as N_vendite
         FROM product p
         JOIN category c ON p.category_id = c.id
         JOIN order_item o ON p.id = o.product_id
         JOIN `order` o1 ON o1.id = o.order_id
         WHERE c.category_name = %s AND o1.order_date BETWEEN %s AND %s
        GROUP BY p.id, p.product_name
         ORDER BY product_name 
         """

        cursor.execute(query, (category, first, last,))
        for row in cursor:
            result.append((row["product_name"], row["id"], row["N_vendite"]))

        cursor.close()
        conn.close()
        return result


if __name__=="__main__":
    k= DAO.get_product_in_category("Road Bikes", '2016-01-01 00:00:00', '2018-12-28 00:00:00')
    for x in k:
        print(x)