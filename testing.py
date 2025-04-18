from sqlalchemy import desc, func, select
from sqlalchemy.orm import Session


from crud.stats import (
    get_best_rated_boulders,
    get_most_repeated_boulders,
    get_hardest_boulders,
    get_grade_distribution,
    get_boulders_rating_distribution,
    get_repeats_volume_distribution,
    get_style_distribution,
    get_top_repeaters,
    get_top_setters,
)
from database import engine
from models.area import Area
from models.boulder import Boulder
from models.repetition import Repetition
from models.boulder_setter import boulder_setter_table
from models.user import User

if __name__ == "__main__":
    session = Session(engine)
    print(
        session.scalar(select(func.count(func.distinct(Repetition.user_id))))
    )
    print(
        session.scalar(
            select(func.count(func.distinct(boulder_setter_table.c.user_id)))
        )
    )
    print(
        session.scalar(
            select(func.count(User.id))
            .outerjoin(Repetition, User.id == Repetition.user_id)
            .where(Repetition.user_id.is_(None))
        )
    )
        
    result = get_repeats_volume_distribution(session)
    for line in result:
        print(line)

    # import matplotlib.pyplot as plt

    # # Your data: each tuple is (rating, frequency)
    # data = [
    #     ("P", 25),
    #     ("1", 782),
    #     ("1+", 169),
    #     ("2-", 445),
    #     ("2", 1595),
    #     ("2+", 1296),
    #     ("3-", 1300),
    #     ("3", 1463),
    #     ("3+", 1486),
    #     ("4-", 1521),
    #     ("4", 1743),
    #     ("4+", 1657),
    #     ("5-", 1493),
    #     ("5", 2158),
    #     ("5+", 2277),
    #     ("6a", 2455),
    #     ("6a+", 1068),
    #     ("6b", 2242),
    #     ("6b+", 1164),
    #     ("6c", 2446),
    #     ("6c+", 1215),
    #     ("7a", 3233),
    #     ("7a+", 2000),
    #     ("7b", 1718),
    #     ("7b+", 1123),
    #     ("7c", 877),
    #     ("7c+", 530),
    #     ("8a", 417),
    #     ("8a+", 162),
    #     ("8b", 92),
    #     ("8b+", 48),
    #     ("8c", 23),
    #     ("8c+", 8),
    #     ("9a", 4),
    # ]

    # # Separate the data into ratings and frequencies
    # ratings, frequencies = zip(*data)

    # # Create a bar chart
    # plt.figure(figsize=(12, 6))
    # plt.bar(
    #     ratings,
    #     frequencies,
    #     width=0.05,
    #     align="center",
    #     color="skyblue",
    #     edgecolor="black",
    # )
    # plt.xlabel("Rating")
    # plt.ylabel("Frequency")
    # plt.title("Histogram of Boulder Ratings")
    # plt.xticks(ratings, rotation=45)  # rotate x labels if needed
    # plt.grid(axis="y", linestyle="--", alpha=0.7)
    # plt.tight_layout()
    # plt.show()
