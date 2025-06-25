from database.DB_connect import DBConnect
from model.order import Order


class DAO():

    @staticmethod
    def getAllStoreId():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select store_id
                    from stores
                    order by store_id"""
        cursor.execute(query)
        for row in cursor:
            result.append(row["store_id"])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllOrdersByStoreId(storeId):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from orders
                    where store_id = %s"""
        cursor.execute(query, (storeId,))
        for row in cursor:
            result.append(Order(**row))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllEdges(storeId, nMaxGiorni):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t2.order_id as nodoPartenza, t1.order_id as nodoArrivo, (t1.somma + t2.somma) as peso
                    from (select o.order_id, o.order_date, sum(oi.quantity) as somma 
                            from orders o, order_items oi
                            where o.store_id =%s and o.order_id = oi.order_id
                            group by o.order_id, o.order_date
                            ) t1, 
                         (select o.order_id, o.order_date, sum(oi.quantity) as somma 
                            from orders o, order_items oi
                            where o.store_id =%s and o.order_id = oi.order_id
                            group by o.order_id, o.order_date
                            ) t2
                    where t1.order_id < t2.order_id and datediff(t2.order_date, t1.order_date) < %s and datediff(t2.order_date, t1.order_date) > 0"""
        cursor.execute(query, (storeId, storeId, nMaxGiorni))
        for row in cursor:
            result.append((row["nodoPartenza"], row["nodoArrivo"], row["peso"]))
        cursor.close()
        conn.close()
        return result