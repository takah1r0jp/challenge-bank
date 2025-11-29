"""
既存のusersテーブルにis_notification_setup_completedカラムを追加するスクリプト
"""

from sqlalchemy import create_engine, text

from database import SQLALCHEMY_DATABASE_URL


def add_notification_setup_column():
    """usersテーブルにis_notification_setup_completedカラムを追加"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

    with engine.connect() as conn:
        # カラムの存在確認
        result = conn.execute(
            text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='is_notification_setup_completed'
        """)
        )

        if result.fetchone():
            print("✅ カラム 'is_notification_setup_completed' は既に存在します")
            return

        # カラムを追加
        conn.execute(
            text("""
            ALTER TABLE users
            ADD COLUMN is_notification_setup_completed BOOLEAN NOT NULL DEFAULT FALSE
        """)
        )
        conn.commit()

        print("✅ カラム 'is_notification_setup_completed' を追加しました")
        print("   - 型: BOOLEAN")
        print("   - デフォルト値: FALSE")
        print("   - NOT NULL制約: あり")


if __name__ == "__main__":
    add_notification_setup_column()
