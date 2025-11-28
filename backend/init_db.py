# モデルをインポートしてBaseに登録
import models  # noqa: F401
from database import Base, engine

# テーブル作成
Base.metadata.create_all(bind=engine)

print("テーブルを作成しました:")
print("- users")
print("- challenges")
