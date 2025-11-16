from database import Base, engine

# モデルをインポートしてBaseに登録
import models  # noqa: F401

# テーブル作成
Base.metadata.create_all(bind=engine)

print("テーブルを作成しました:")
print("- users")
print("- failures")
