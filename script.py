import cleaner.recipeCleaner as rc
import combiners.combineMarketUsda as comb
import combiners.combineRawRecipe as combrawrec
import cleaner.marketCleaner as mc
import normalizers.masterRel as mr
import normalizers.normMap as nma
import normalizers.normRaw as nra
import normalizers.normRecipe as nre
import normalizers.normCounties as nco
import migrators.migrateSqlite as mig


# consumers


# cleaners
rc.recipe_cleaner()
mc.market_cleaner()


# combiners
comb.combineMarketUsda()
combrawrec.combineRawRecipe()

# normalizers
mr.master_rel()
nma.norm_map()
nra.norm_raw()
nre.norm_recipe()
nco.county_shape()

# migrators
mig.make_migrations()

# if __name__ == '__main__':
#     pass
