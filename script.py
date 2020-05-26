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
print('Starting Cleaners')
rc.recipe_cleaner()
mc.market_cleaner()


# combiners
print('Starting Combiners')
comb.combineMarketUsda()
combrawrec.combineRawRecipe()

# normalizers
print('Starting Normalizers')
mr.master_rel()
nma.norm_map()
nra.norm_raw()
nre.norm_recipe()
nco.county_shape()

# migrators
print('Migrating to sqlite DB')
mig.make_migrations()


print("""

 /$$      /$$ /$$$$$$$$ /$$        /$$$$$$   /$$$$$$  /$$      /$$ /$$$$$$$$       /$$$$$$$$ /$$$$$$        
| $$  /$ | $$| $$_____/| $$       /$$__  $$ /$$__  $$| $$$    /$$$| $$_____/      |__  $$__//$$__  $$       
| $$ /$$$| $$| $$      | $$      | $$  \__/| $$  \ $$| $$$$  /$$$$| $$               | $$  | $$  \ $$       
| $$/$$ $$ $$| $$$$$   | $$      | $$      | $$  | $$| $$ $$/$$ $$| $$$$$            | $$  | $$  | $$       
| $$$$_  $$$$| $$__/   | $$      | $$      | $$  | $$| $$  $$$| $$| $$__/            | $$  | $$  | $$       
| $$$/ \  $$$| $$      | $$      | $$    $$| $$  | $$| $$\  $ | $$| $$               | $$  | $$  | $$       
| $$/   \  $$| $$$$$$$$| $$$$$$$$|  $$$$$$/|  $$$$$$/| $$ \/  | $$| $$$$$$$$         | $$  |  $$$$$$/       
|__/     \__/|________/|________/ \______/  \______/ |__/     |__/|________/         |__/   \______/        
                                                                                                            
                                                                                                            
                                                                                                            
 /$$$$$$$$                                       /$$                     /$$$$$$$$                          
| $$_____/                                      | $$                    | $$_____/                          
| $$    /$$$$$$   /$$$$$$  /$$$$$$/$$$$        /$$$$$$    /$$$$$$       | $$    /$$$$$$   /$$$$$$$  /$$$$$$ 
| $$$$$|____  $$ /$$__  $$| $$_  $$_  $$      |_  $$_/   /$$__  $$      | $$$$$|____  $$ /$$_____/ /$$__  $$
| $$__/ /$$$$$$$| $$  \__/| $$ \ $$ \ $$        | $$    | $$  \ $$      | $$__/ /$$$$$$$| $$      | $$$$$$$$
| $$   /$$__  $$| $$      | $$ | $$ | $$        | $$ /$$| $$  | $$      | $$   /$$__  $$| $$      | $$_____/
| $$  |  $$$$$$$| $$      | $$ | $$ | $$        |  $$$$/|  $$$$$$/      | $$  |  $$$$$$$|  $$$$$$$|  $$$$$$$
|__/   \_______/|__/      |__/ |__/ |__/         \___/   \______/       |__/   \_______/ \_______/ \_______/

""")
