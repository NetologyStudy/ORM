from orm import SyncORM
SyncORM.create_tables()
SyncORM.insert_publisher()
SyncORM.insert_book()
SyncORM.insert_shop()
SyncORM.insert_stock()
SyncORM.insert_sale()

if __name__ == "__main__":
    # Информация только для Пушкина, поэтому используем имя - Пушкин:)
    author_name = input("Введите имя автора (издателя): ").strip()
    sales_data = SyncORM.get_sales_by_publisher(author_name)

    if sales_data:
        for idx, row in enumerate(sales_data, 1):
            print(f"{idx}. {row[0]} | {row[1]} | {row[2]} руб. | {row[3]}")
    else:
        print("Книг данного автора не найдено в продажах.")