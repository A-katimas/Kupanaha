NAME = a_maze_ing.py

OBJ = $(SOURCE:.c=.o)


install:
	

run:
	uv run python3 $(NAME)

debug:

clean:
	rm -rf $(OBJ)


re: fclean all

.PHONY : all clean fclean re