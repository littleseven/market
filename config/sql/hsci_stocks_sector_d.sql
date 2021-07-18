create view hsci_stocks_sector_d as
SELECT
	`t`.`date` AS `date`,
	round(max(`t`.`MAT`), 0) AS `MAT`,
	round(max(`t`.`COM`), 0) AS `COM`,
	round(max(`t`.`CNS`), 0) AS `CNS`,
	round(max(`t`.`CND`), 0) AS `CND`,
	round(max(`t`.`ENE`), 0) AS `ENE`,
	round(max(`t`.`FIN`), 0) AS `FIN`,
	round(max(`t`.`HLT`), 0) AS `HLT`,
	round(max(`t`.`IND`), 0) AS `IND`,
	round(max(`t`.`REI`), 0) AS `REI`,
	round(max(`t`.`TEC`), 0) AS `TEC`,
	round(max(`t`.`UTL`), 0) AS `UTL`,
	round(
		(
			(
				(
					(
						(
							(
								(
									(
										(
											(
												(
													max(`t`.`MAT`) + max(`t`.`COM`)
												) + max(`t`.`CNS`)
											) + max(`t`.`CND`)
										) + max(`t`.`ENE`)
									) + max(`t`.`FIN`)
								) + max(`t`.`HLT`)
							) + max(`t`.`IND`)
						) + max(`t`.`REI`)
					) + max(`t`.`TEC`)
				) + max(`t`.`UTL`)
			) / 11
		),
		0
	) AS `HSC`,
	round(
		(
			(
				(
					(
						(
							(
								(
									(
										(
											(
												(
													max(`t`.`MAT`) + max(`t`.`COM`)
												) + max(`t`.`CNS`)
											) + max(`t`.`CND`)
										) + max(`t`.`ENE`)
									) + max(`t`.`FIN`)
								) + max(`t`.`HLT`)
							) + max(`t`.`IND`)
						) + max(`t`.`REI`)
					) + max(`t`.`TEC`)
				) + max(`t`.`UTL`)
			)
		),
		0
	) AS `SUM`
FROM
	(
		SELECT
			`t`.`date` AS `date`,
			(
				CASE
				WHEN (`t`.`sector` = 'Materials') THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `MAT`,
			(
				CASE
				WHEN (
					`t`.`sector` = 'Communication Services'
				) THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `COM`,
			(
				CASE
				WHEN (
					`t`.`sector` = 'Consumer Staples'
				) THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `CNS`,
			(
				CASE
				WHEN (
					`t`.`sector` = 'Consumer Discretionary'
				) THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `CND`,
			(
				CASE
				WHEN (`t`.`sector` = 'Energy') THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `ENE`,
			(
				CASE
				WHEN (`t`.`sector` = 'Financials') THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `FIN`,
			(
				CASE
				WHEN (`t`.`sector` = 'Health Care') THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `HLT`,
			(
				CASE
				WHEN (`t`.`sector` = 'Industrials') THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `IND`,
			(
				CASE
				WHEN (`t`.`sector` = 'Real Estate') THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `REI`,
			(
				CASE
				WHEN (
					`t`.`sector` = 'Information Technology'
				) THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `TEC`,
			(
				CASE
				WHEN (`t`.`sector` = 'Utilities') THEN
					(
						(
							sum(`t`.`is_above_s_ma`) / count(DISTINCT `t`.`code`)
						) * 100
					)
				END
			) AS `UTL`
		FROM
			(
				SELECT
					`t1`.`date` AS `date`,
					`t1`.`code` AS `code`,
					`t1`.`sp_sector` AS `sector`,
					`t1`.`is_above_s_ma` AS `is_above_s_ma`
				FROM
					(
						SELECT
							`hsc_stocks_d`.`date` AS `date`,
							`hsc_stocks_d`.`code` AS `code`,
							`hsc_stocks_d`.`name` AS `name`,
							`hsc_stocks_d`.`sector` AS `sector`,
							`hsc_stocks_d`.`sp_sector` AS `sp_sector`,
							`hsc_stocks_d`.`industry` AS `industry`,
							`hsc_stocks_d`.`total_cap` AS `total_cap`,
							`hsc_stocks_d`.`is_ss` AS `is_ss`,
							`hsc_stocks_d`.`is_sz` AS `is_sz`,
							`hsc_stocks_d`.`is_hs` AS `is_hs`,
							`hsc_stocks_d`.`weight` AS `weight`,
							`hsc_stocks_d`.`open` AS `open`,
							`hsc_stocks_d`.`high` AS `high`,
							`hsc_stocks_d`.`low` AS `low`,
							`hsc_stocks_d`.`close` AS `close`,
							`hsc_stocks_d`.`pre_close` AS `pre_close`,
							`hsc_stocks_d`.`is_gap` AS `is_gap`,
							`hsc_stocks_d`.`vol` AS `vol`,
							`hsc_stocks_d`.`ma_vol` AS `ma_vol`,
							`hsc_stocks_d`.`vol_rate` AS `vol_rate`,
							`hsc_stocks_d`.`s_ma` AS `s_ma`,
							`hsc_stocks_d`.`m_ma` AS `m_ma`,
							`hsc_stocks_d`.`l_ma` AS `l_ma`,
							`hsc_stocks_d`.`s_ema` AS `s_ema`,
							`hsc_stocks_d`.`m_ema` AS `m_ema`,
							`hsc_stocks_d`.`l_ema` AS `l_ema`,
							`hsc_stocks_d`.`cs` AS `cs`,
							`hsc_stocks_d`.`pcs` AS `pcs`,
							`hsc_stocks_d`.`is_cs_over` AS `is_cs_over`,
							`hsc_stocks_d`.`sm` AS `sm`,
							`hsc_stocks_d`.`psm` AS `psm`,
							`hsc_stocks_d`.`is_sm_over` AS `is_sm_over`,
							`hsc_stocks_d`.`ml` AS `ml`,
							`hsc_stocks_d`.`pml` AS `pml`,
							`hsc_stocks_d`.`is_ml_over` AS `is_ml_over`,
							`hsc_stocks_d`.`bais` AS `bais`,
							`hsc_stocks_d`.`ecs` AS `ecs`,
							`hsc_stocks_d`.`esm` AS `esm`,
							`hsc_stocks_d`.`pesm` AS `pesm`,
							`hsc_stocks_d`.`is_esm_over` AS `is_esm_over`,
							`hsc_stocks_d`.`eml` AS `eml`,
							`hsc_stocks_d`.`peml` AS `peml`,
							`hsc_stocks_d`.`is_eml_over` AS `is_eml_over`,
							`hsc_stocks_d`.`ebais` AS `ebais`,
							`hsc_stocks_d`.`s_close` AS `s_close`,
							`hsc_stocks_d`.`s_pre_close` AS `s_pre_close`,
							`hsc_stocks_d`.`is_s_up` AS `is_s_up`,
							`hsc_stocks_d`.`m_close` AS `m_close`,
							`hsc_stocks_d`.`m_pre_close` AS `m_pre_close`,
							`hsc_stocks_d`.`is_m_up` AS `is_m_up`,
							`hsc_stocks_d`.`l_close` AS `l_close`,
							`hsc_stocks_d`.`l_pre_close` AS `l_pre_close`,
							`hsc_stocks_d`.`is_l_up` AS `is_l_up`,
							(
								CASE
								WHEN (
									`hsc_stocks_d`.`close` > `hsc_stocks_d`.`s_ma`
								) THEN
									1
								ELSE
									0
								END
							) AS `is_above_s_ma`
						FROM
							`hsc_stocks_d`
						WHERE
							(
								`hsc_stocks_d`.`date` >= CONVERT (
									date_format(
										(now() - INTERVAL 6 MONTH),
										'%Y-%m-%d'
									) USING utf8mb4
								)
							)
					) `t1`
			) `t`
		WHERE
			(`t`.`sector` IS NOT NULL)
		GROUP BY
			`t`.`date`,
			`t`.`sector`
	) `t`
GROUP BY
	`t`.`date`
ORDER BY
	`t`.`date` DESC
;