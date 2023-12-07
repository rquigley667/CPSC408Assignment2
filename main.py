import mysql.connector
import sys

#34.145.118.100
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password="change-me",
            database='Assignment2'
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL:{e}")
        return None

def Out_of_stock_Products(conn):
    try:
        cursor = conn.cursor()
        query = "SELECT ProductId, ProductName, UnitsInStock FROM Products"
        cursor.execute(query)
        out_of_stock_products = []

        for row in cursor.fetchall():
            product_id, product_name, units_in_stock = row
            if units_in_stock == 0:
                out_of_stock_products.append(product_name)

        if out_of_stock_products:
            print("The Products Out of stock are:", out_of_stock_products)
        else:
            print("No products are out of stock.\n")

    except mysql.connector.Error as e:
        print(f"Error displaying Products: {e}")


def Total_Number_Orders_Placed(conn):
    try:
        cursor = conn.cursor()
        query = ("""
                    SELECT
                        Customers.CustomerID,
                        Customers.CustomerName,
                        COUNT(Orders.OrderID) AS TotalOrders
                    FROM
                        Customers
                    LEFT JOIN
                        Orders ON Customers.CustomerID = Orders.CustomerID
                    GROUP BY
                        Customers.CustomerID, Customers.CustomerName
                """)

        cursor.execute(query)
        results = cursor.fetchall()

        # Display the results
        for row in results:
            customer_id, customer_name, total_orders = row
            print(f"Customer {customer_id} ({customer_name}): {total_orders} orders\n")


    except mysql.connector.Error as e:
        print(f"Error executing the query: {e}")

    finally:
        cursor.close()



def See_Details_Of_Most_Expensive_Product_In_Each_Order(conn):
    try:
        cursor = conn.cursor()
        query = ("""
                SELECT
                    o.OrderID,
                    p.ProductID,
                    p.ProductName,
                    od.UnitPrice,
                    od.Quantity
                FROM
                    Orders o
                JOIN
                    OrderDetails od ON o.OrderID = od.OrderID
                JOIN
                    Products p ON od.ProductID = p.ProductID
                WHERE (o.OrderID, od.UnitPrice) IN (
                    SELECT OrderID, MAX(UnitPrice)
                    FROM OrderDetails
                    GROUP BY OrderID)
                ORDER BY o.OrderID;
            """)

        cursor.execute(query)

        results = cursor.fetchall()
        for row in results:
            order_id, product_id, product_name, max_unit_price, quantity = row
            print(f"Order ID: {order_id}, Product ID: {product_id}, Product Name: {product_name}, Max Unit Price: {max_unit_price}, Quantity: {quantity}")

    except mysql.connector.Error as e:
        print(f"Error executing the query: {e}")
    finally:
        cursor.close()




import mysql.connector

def products_never_ordered(conn):
    try:
        cursor = conn.cursor()

        # Execute the SQL query
        query = """
            SELECT Products.ProductID, Products.ProductName
            FROM Products
            LEFT JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
            WHERE OrderDetails.OrderID IS NULL AND OrderDetails.ProductID IS NULL;
        """
        cursor.execute(query)

        # Fetch the results
        never_ordered_products = cursor.fetchall()

        # Print the results
        for product in never_ordered_products:
            print(f"Product ID: {product[0]}, Product Name: {product[1]}")

    except mysql.connector.Error as e:
        print(f"Error executing the query: {e}")

    finally:
        # Close the cursor
        cursor.close()


def total_revenue_by_supplier(conn):
    try:
        cursor = conn.cursor()

        # Execute the SQL query
        query = """
            SELECT Suppliers.SupplierID, Suppliers.SupplierName,
                   SUM(Products.UnitPrice * OrderDetails.Quantity) AS TotalRevenue
            FROM Suppliers
            INNER JOIN Products ON Suppliers.SupplierID = Products.SupplierID
            LEFT JOIN OrderDetails ON Products.ProductID = OrderDetails.ProductID
            GROUP BY Suppliers.SupplierID, Suppliers.SupplierName;
        """
        cursor.execute(query)

        # Fetch the results
        total_revenue_by_supplier = cursor.fetchall()

        # Print the results
        for row in total_revenue_by_supplier:
            print(f"Supplier {row[0]} ({row[1]}): Total Revenue ${row[2]}")

    except mysql.connector.Error as e:
        print(f"Error executing the query: {e}")

    finally:
        # Close the cursor
        cursor.close()



def Exit_Program():

    print("Exiting out of the application")
    sys.exit(0)

def main():
    conn = connect_to_database()
    #if conn:
        #Out_of_stock_Products(conn,product_id, product_name,units_in_stock)
        #conn.close()


    while True:
        print("Press 1 to List the products that are out of stock.\n"
                       "Press 2 to Find total number of orders placed by each customer.\n"
                       "Press 3 to see the details of the most expensive product orderd in each order.\n"
                       "Press 4 to see a list of products that have never been ordered.\n"
                       "Press 5 to see the total revenue by each supplier.\n"
                       "Press 6 to Exit the program.\n")
        UserOptionSelected = int(input("You want: "))

        if UserOptionSelected == 1:
            Out_of_stock_Products(conn)
        elif UserOptionSelected == 2:
            Total_Number_Orders_Placed(conn)
        elif UserOptionSelected == 3:
            See_Details_Of_Most_Expensive_Product_In_Each_Order(conn)
        elif UserOptionSelected == 4:
            products_never_ordered(conn)
        elif UserOptionSelected == 5:
            total_revenue_by_supplier(conn)
        elif UserOptionSelected == 6:
            Exit_Program()
        else:
            print("Choose one of these options!!")

if __name__ == "__main__":
    main()
