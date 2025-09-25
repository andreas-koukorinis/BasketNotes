Create a comprehensive basket_types.py file that serves as the core data structures and constants layer for a bond basket construction system. This file should:

**Core Requirements:**
- Define standardized column names and data types for bond data
- Create structured input/output data classes using @dataclass
- Implement validation schemas for different basket types
- Provide filter type definitions and validation
- Include constants for rating scales, sector classifications, duration buckets

**Key Components to Implement:**

1. **TradingSchema class** - Define standard column mappings and types:
   - Required columns: ISIN, sector, rating, duration, liquidity_score, amount_outstanding
   - Optional columns: price, yield, duration_bucket, maturity_date
   - Data type specifications and validation rules

2. **BasketInput dataclass** - Structured input for basket construction:
   - universe: pd.DataFrame
   - basket_type: enum
   - filters: Dict[str, Any]
   - weighting_method: enum
   - constraints: ConstraintConfig

3. **BasketOutput dataclass** - Structured output with metadata:
   - basket_id: str
   - constituents: pd.DataFrame with weights
   - metadata: comprehensive basket statistics
   - quality_metrics: risk and diversification measures
   - warnings: List[str]

4. **Filter enums and validation**:
   - SectorFilter, RatingFilter, DurationFilter classes
   - FilterValidator for input validation
   - Business rule constraints

5. **Constants and mappings**:
   - VALID_RATINGS: Rating hierarchy and categories
   - SECTOR_MAPPINGS: Sector standardization
   - DURATION_BUCKETS: Duration bucket definitions
   - DEFAULT_CONSTRAINTS: Default limits and thresholds

**Technical Requirements:**
- Use Python 3.9+ features (dataclasses, type hints, enums)
- Include comprehensive validation with meaningful error messages
- Support serialization to/from JSON for configuration persistence
- Implement __post_init__ validation in dataclasses
- Use Pydantic-style validation patterns where appropriate

The file should be the single source of truth for all data structures used across the basket construction system.

data_prep_basket.py
Refactor data_prep_basket.py to implement a TradingSchema-based data preparation pipeline that integrates with the data structures defined in basket_types.py.

**Architecture Requirements:**
- Import and use TradingSchema from basket_types.py for column standardization
- Remove LiquidityCalculator (liquidity is pre-computed)
- Implement UniverseFilter that works with TradingSchema
- Focus on data validation, normalization, and universe construction

**Key Classes to Implement:**

1. **TradingSchemaValidator**:
   - Validate incoming DataFrames against TradingSchema requirements
   - Check required columns, data types, value ranges
   - Generate DataQualityReport with detailed validation results
   - Handle missing data strategies (drop, fill, warn)

2. **UniverseFilter** (TradingSchema-based):
   - filter_by_schema(df, schema) -> apply base trading rules
   - filter_by_liquidity_percentile(df, min_percentile) 
   - filter_by_sector(df, allowed_sectors)
   - filter_by_rating_range(df, min_rating, max_rating)
   - filter_for_similarity(df, reference_isin, criteria) -> similarity constraints
   - Each method should preserve schema compliance

3. **BondDataProcessor** (main orchestrator):
   - process_universe(raw_df, trading_schema) -> (clean_df, quality_report)
   - standardize_to_schema(df, schema) -> apply column mappings and types
   - validate_universe_quality(df) -> comprehensive data quality checks
   - enrich_with_derived_features(df) -> add computed columns (rating_category, size_bucket, etc.)

4. **DataQualityReport dataclass**:
   - Schema compliance metrics
   - Missing data summary by column
   - Outlier detection results  
   - Data type conversion issues
   - Actionable recommendations for data quality improvement

**Integration Points:**
- Use BasketInput.universe as the primary data container
- Leverage TradingSchema for all column name standardization
- Return processed data in schema-compliant format
- Generate warnings that integrate with BasketOutput.warnings

**Performance Requirements:**
- Optimize pandas operations for large datasets (100k+ bonds)
- Use vectorized operations for all filtering
- Memory-efficient data processing patterns
- Lazy evaluation where possible

The module should serve as the data gateway that ensures all downstream basket construction works with clean, schema-compliant data.

Implement basket_construction.py as the core business logic layer that uses data structures from basket_types.py and processes data from data_prep_basket.py.

**Architecture Requirements:**
- Import and use BasketInput, BasketOutput, and other data classes from basket_types
- Implement Strategy pattern for different weighting methods
- Use composition with clear separation of concerns
- All methods should accept/return structured data classes

**Key Components to Implement:**

1. **WeightingStrategy ABC and implementations**:
   - EqualWeightStrategy: weights = 1/n for all positions
   - AmountOutstandingWeightStrategy: weights ∝ amount_outstanding
   - LiquidityWeightStrategy: weights ∝ liquidity_score with power parameter
   - CustomWeightStrategy: user-defined weighting function
   - Each strategy validates required columns and handles edge cases

2. **BasketConstructor** (main orchestrator):
   - build_basket(basket_input: BasketInput) -> BasketOutput
   - Delegate to specialized builders based on basket_input.basket_type
   - Apply weighting strategy from basket_input.weighting_method
   - Validate constraints from basket_input.constraints
   - Generate comprehensive BasketOutput with metadata

3. **Specialized basket builders**:
   - SectorBasketBuilder(universe, sector, size_limit)
   - SectorRatingBasketBuilder(universe, sector, rating, size_limit)  
   - SectorRatingDurationBasketBuilder(universe, sector, rating, duration_bucket, size_limit)
   - SimilarityBasketBuilder(universe, reference_isin, similarity_params)

4. **SimilarityMatcher**:
   - find_similar_bonds(universe, reference_isin, criteria) -> filtered DataFrame
   - calculate_similarity_scores() using duration, rating, sector, liquidity
   - apply_similarity_constraints() with tolerance parameters
   - rank_by_similarity() for final selection

5. **ConstraintValidator**:
   - validate_basket_constraints(constituents, weights, constraints) -> violations list
   - Check size limits, concentration limits, diversification requirements
   - Generate actionable constraint violation messages
   - Suggest remediation strategies

6. **QualityMetricsCalculator**:
   - calculate_portfolio_metrics(constituents, weights) -> comprehensive metrics dict
   - Duration, sector, rating diversification measures
   - Concentration metrics (Herfindahl index, effective N positions)
   - Liquidity and size distribution statistics

**Method Signatures:**
```python
def build_basket(basket_input: BasketInput) -> BasketOutput:
def calculate_weights(bonds: pd.DataFrame, method: WeightingMethod, **params) -> pd.Series:
def find_similar_bonds(universe: pd.DataFrame, reference_isin: str, config: SimilarityConfig) -> pd.DataFrame:
def validate_constraints(basket_output: BasketOutput) -> List[ConstraintViolation]:

Implement basket_construction.py as the core business logic layer that uses data structures from basket_types.py and processes data from data_prep_basket.py.

**Architecture Requirements:**
- Import and use BasketInput, BasketOutput, and other data classes from basket_types
- Implement Strategy pattern for different weighting methods
- Use composition with clear separation of concerns
- All methods should accept/return structured data classes

**Key Components to Implement:**

1. **WeightingStrategy ABC and implementations**:
   - EqualWeightStrategy: weights = 1/n for all positions
   - AmountOutstandingWeightStrategy: weights ∝ amount_outstanding
   - LiquidityWeightStrategy: weights ∝ liquidity_score with power parameter
   - CustomWeightStrategy: user-defined weighting function
   - Each strategy validates required columns and handles edge cases

2. **BasketConstructor** (main orchestrator):
   - build_basket(basket_input: BasketInput) -> BasketOutput
   - Delegate to specialized builders based on basket_input.basket_type
   - Apply weighting strategy from basket_input.weighting_method
   - Validate constraints from basket_input.constraints
   - Generate comprehensive BasketOutput with metadata

3. **Specialized basket builders**:
   - SectorBasketBuilder(universe, sector, size_limit)
   - SectorRatingBasketBuilder(universe, sector, rating, size_limit)  
   - SectorRatingDurationBasketBuilder(universe, sector, rating, duration_bucket, size_limit)
   - SimilarityBasketBuilder(universe, reference_isin, similarity_params)

4. **SimilarityMatcher**:
   - find_similar_bonds(universe, reference_isin, criteria) -> filtered DataFrame
   - calculate_similarity_scores() using duration, rating, sector, liquidity
   - apply_similarity_constraints() with tolerance parameters
   - rank_by_similarity() for final selection

5. **ConstraintValidator**:
   - validate_basket_constraints(constituents, weights, constraints) -> violations list
   - Check size limits, concentration limits, diversification requirements
   - Generate actionable constraint violation messages
   - Suggest remediation strategies

6. **QualityMetricsCalculator**:
   - calculate_portfolio_metrics(constituents, weights) -> comprehensive metrics dict
   - Duration, sector, rating diversification measures
   - Concentration metrics (Herfindahl index, effective N positions)
   - Liquidity and size distribution statistics

**Method Signatures:**
```python
def build_basket(basket_input: BasketInput) -> BasketOutput:
def calculate_weights(bonds: pd.DataFrame, method: WeightingMethod, **params) -> pd.Series:
def find_similar_bonds(universe: pd.DataFrame, reference_isin: str, config: SimilarityConfig) -> pd.DataFrame:
def validate_constraints(basket_output: BasketOutput) -> List[ConstraintViolation]:

Refactor data_prep_basket.py to implement a TradingSchema-based data preparation pipeline that integrates with the data structures defined in basket_types.py.

**Architecture Requirements:**
- Import and use TradingSchema from basket_types.py for column standardization
- Remove LiquidityCalculator (liquidity is pre-computed)
- Implement UniverseFilter that works with TradingSchema
- Focus on data validation, normalization, and universe construction

**Key Classes to Implement:**

1. **TradingSchemaValidator**:
   - Validate incoming DataFrames against TradingSchema requirements
   - Check required columns, data types, value ranges
   - Generate DataQualityReport with detailed validation results
   - Handle missing data strategies (drop, fill, warn)

2. **UniverseFilter** (TradingSchema-based):
   - filter_by_schema(df, schema) -> apply base trading rules
   - filter_by_liquidity_percentile(df, min_percentile) 
   - filter_by_sector(df, allowed_sectors)
   - filter_by_rating_range(df, min_rating, max_rating)
   - filter_for_similarity(df, reference_isin, criteria) -> similarity constraints
   - Each method should preserve schema compliance

3. **BondDataProcessor** (main orchestrator):
   - process_universe(raw_df, trading_schema) -> (clean_df, quality_report)
   - standardize_to_schema(df, schema) -> apply column mappings and types
   - validate_universe_quality(df) -> comprehensive data quality checks
   - enrich_with_derived_features(df) -> add computed columns (rating_category, size_bucket, etc.)

4. **DataQualityReport dataclass**:
   - Schema compliance metrics
   - Missing data summary by column
   - Outlier detection results  
   - Data type conversion issues
   - Actionable recommendations for data quality improvement

**Integration Points:**
- Use BasketInput.universe as the primary data container
- Leverage TradingSchema for all column name standardization
- Return processed data in schema-compliant format
- Generate warnings that integrate with BasketOutput.warnings

**Performance Requirements:**
- Optimize pandas operations for large datasets (100k+ bonds)
- Use vectorized operations for all filtering
- Memory-efficient data processing patterns
- Lazy evaluation where possible

The module should serve as the data gateway that ensures all downstream basket construction works with clean, schema-compliant data.
