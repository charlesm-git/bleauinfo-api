from sqlalchemy import Float, cast, desc, func, select
from sqlalchemy.orm import Session


from crud.stats import (
    get_best_rated_boulders,
    get_most_repeated_boulders,
    get_hardest_boulders,
    get_grade_distribution,
    get_boulders_rating_distribution,
    get_repeats_per_month,
    get_repeats_per_year,
    get_repeats_volume_distribution,
    get_style_distribution,
    get_top_repeaters,
    get_top_setters,
)
from database import engine
from models.area import Area
from models.boulder import Boulder
from models.grade import Grade
from models.repetition import Repetition
from models.boulder_setter import boulder_setter_table
from models.user import User

if __name__ == "__main__":
    session = Session(engine)

    # print(
    #     session.execute(
    #         select(
    #             func.strftime("%Y-%m", Repetition.log_date).label("date"),
    #             func.count(Repetition.user_id).label("count"),
    #         )
    #         .order_by(desc("count"))
    #         .group_by("date")
    #         .limit(20)
    #     ).all()
    # )
    result = (
        session.execute(
            select(Grade.value, func.count(Repetition.user_id))
            .join(Boulder, Boulder.grade_id == Grade.id)
            .join(Repetition, Repetition.boulder_id == Boulder.id)
            .group_by(Grade.correspondence)
            .order_by(Grade.correspondence)
        ).all()
    )
    print(result)

    import matplotlib.pyplot as plt

    # Your data: each tuple is (rating, frequency)
    data = result

    # Separate the data into ratings and frequencies
    ratings, frequencies = zip(*data)

    # Create a bar chart
    plt.figure(figsize=(12, 6))
    plt.bar(
        ratings,
        frequencies,
        width=0.05,
        align="center",
        color="skyblue",
        edgecolor="black",
    )
    plt.xlabel("Rating")
    plt.ylabel("Frequency")
    plt.title("Histogram of Boulder Ratings")
    plt.xticks(ratings, rotation=45)  # rotate x labels if needed
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()
