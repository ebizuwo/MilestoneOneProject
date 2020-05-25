import cleaner.recipeCleaner as rc
import combiners.combineMarketUsda as comb
import combiners.combineRawRecipe as combrawrec
import cleaner.marketCleaner as mc

# consumers


# cleaners
rc.recipe_cleaner()
mc.market_cleaner()


# combiners
comb.combineMarketUsda()
combrawrec.combineRawRecipe()



# if __name__ == '__main__':
#     pass
