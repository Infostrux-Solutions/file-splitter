import os
import sys
import logging
import logging.handlers
import argparse
import subprocess
from pathlib import Path


def main(*args):
    """
    This is the main function that will be called by the framework.
    """

    print("------------------------------")
    print("Python environment:")
    print(" executable: ", sys.executable)
    print(" version: ", sys.version.replace("\n", ""))

    parser = argparse.ArgumentParser(prog='merge')
    parser.add_argument('--HELP', action='store_true')

    args = parser.parse_args()

    if not args.HELP: 
        """
        """

        metadata_loader = BAMMetadataLoader()
        entity_id = config.entity_doc_id
        entity_range = config.bam_entity_range_name

        metadata_loader = BAMMetadataLoader(entity_id, entity_range)
        metadata = metadata_loader.load_metadata()

        _overwrite = True
        if os.getenv('MODEL_OVERWRITE').lower() == 'false':
            _overwrite = False
        modelgen = ModelGenerator(  metadata = metadata,
                                    model_path = os.getenv('MODEL_GEN_PATH'),
                                    templates_path = os.getenv('TEMPLATE_FOLDER'),
                                    template_name = os.getenv('TEMPLATE_NAME'),
                                    test_template_name = os.getenv('TEST_TEMPLATE_NAME'),
                                    overwrite = _overwrite,
        )
        modelgen.generate()
            

    else: #TODO need to rewrite help
        print(
            """--ALL : Runs all the functions in the following order:
    1. Get View&Table DDLs
    2. Generate DBT Sources
    3. Generate DBT Models
    4. Copy models to dbt project
            """)
        print(""""
--V, --T, --VT : Generates view & table definitions from snowflake and place them in folder 'snowflake_ddl/database/schema':
    <entity>.sql  
        (as returned by Snowflake function select get_ddl('table', '<database>.<schema>.<table>'))
    <entity>.yml  
        - Will have `description: \<comment>` for columns that have COMMENT attribute set in Snowflake.
        - PK columns will have tests 'dbt_constraints.primary_key'
        - UNIQUE columns will have tests 'dbt_constraints.unique_key'  
        - FOREIGN KEY columns will have tests 'dbt_constraints.foreign_key'
        - Columns with constraint NOT NULL will have 'not_null' tests (unless is already a PK)
        (for more details see README.md or visit 'https://github.com/Snowflake-Labs/dbt_constraints')

        NOTE: append --use_old_yml_syntax argument to revert to classic <entity>.yml syntax (see bellow)

--use_old_yml_syntax : Append at the end of the command line to
    force usage of classic dbt <entity>.yml syntax for tests where
    PK columns will have tests 'unique' and 'not null'
    UNIQUE columns will have tests 'unique'  
    FOREIGN KEY constraints are ignored
--add_dbt_meta : Append at the end of the command line to 
    add "meta:" node to <entity>.yml generated file
    NOTE: applies to commands that generate <entity>.yml files
          including '--ALL', '--VT', '--V', '--T'
    EXAMPLE file: location.yml
... ... ...    
models:
  - name: locations
  meta:
    table_type: "VIEW"
    columns:
      - name: location_id 
        meta:
          data_type: integer
... ... ...

            """)
        print("--HELP or --H : This will print help")
        sys.exit()


if __name__ == '__main__':
    main(*sys.argv[1:])
