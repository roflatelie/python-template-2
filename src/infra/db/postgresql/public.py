import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


meta = sa.MetaData(schema="public")


book = sa.Table(
    "book",
    meta,
    sa.Column("id", UUID(), nullable=False, primary_key=True),
    sa.Column("title", sa.Text, nullable=False),
    sa.Column("ext", sa.Text, nullable=False),
    sa.Column("cover", sa.Text, nullable=False),
    sa.Column("file", sa.Text, nullable=False),
)

author = sa.Table(
    "author",
    meta,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("name", sa.Text, nullable=False),
)

category = sa.Table(
    "category",
    meta,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("name", sa.Text, nullable=False),
    sa.Column("parent_id", sa.BigInteger, nullable=True),
    sa.ForeignKeyConstraint(
        ["parent_id"],
        ["category.id"],
        "category_parent_fk",
        ondelete="CASCADE",
    ),
)

m2m_category_book = sa.Table(
    "m2m_category_book",
    meta,
    sa.Column("book_id", UUID(), nullable=False),
    sa.Column("category_id", sa.BigInteger, nullable=False),
    sa.PrimaryKeyConstraint("book_id", "category_id", name="pk_m2m_category_book"),
    sa.ForeignKeyConstraint(
        ["book_id"],
        ["book.id"],
        "fk_m2m_category_book_on_book",
        ondelete="CASCADE",
    ),
    sa.ForeignKeyConstraint(
        ["category_id"],
        ["category.id"],
        "fk_m2m_category_book_on_category",
        ondelete="CASCADE",
    ),
)

m2m_author_book = sa.Table(
    "m2m_author_book",
    meta,
    sa.Column("book_id", UUID(), nullable=False),
    sa.Column("author_id", sa.BigInteger, nullable=False),
    sa.PrimaryKeyConstraint("book_id", "author_id", name="pk_m2m_author_book"),
    sa.ForeignKeyConstraint(
        ["book_id"],
        ["book.id"],
        "fk_m2m_author_book_on_book",
        ondelete="CASCADE",
    ),
    sa.ForeignKeyConstraint(
        ["author_id"],
        ["author.id"],
        "fk_m2m_author_book_on_author",
        ondelete="CASCADE",
    ),
)
