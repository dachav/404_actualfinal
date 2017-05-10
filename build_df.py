def build_df():
	avg_df = pd.DataFrame(columns= "Cuisine","Average Rating", "Average Sentiment")
	cuisines = get_categories()
	for cuisine in cuisines:
		# for each cuisine calculate the average sentiment and average rating
		rating = avg_rating(cuisine)
		sentiment = get_avg_sentiment(cuisine)
		#populate row of datafram
		avg_df.loc(cuisine) = [cuisine, rating, sentiment]

		return avg_df
