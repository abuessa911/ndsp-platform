# NDSP Checkout + Admin Plans Package

## 1) PostgreSQL Migration

```sh
cd ndsp_checkout_plans_package
DATABASE_URL='postgresql://user:password@127.0.0.1:5432/ndsp' bash scripts/run_migration.sh
