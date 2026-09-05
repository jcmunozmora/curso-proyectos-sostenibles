#!/usr/bin/env bash
# Reconstruye literatura/pdf/ — solo fuentes de acceso abierto.
# Uso: bash recursos/descargar-literatura.sh
set -u
OUT="$(cd "$(dirname "$0")/.." && pwd)/literatura/pdf"
mkdir -p "$OUT" "$OUT/welch-cornell-clima"
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"

get () {
  curl -sL --max-time 300 -A "$UA" -e "https://www.google.com/" -o "$OUT/$1" "$2"
  if [ -s "$OUT/$1" ] && head -c 5 "$OUT/$1" | grep -q '%PDF'; then
    printf "✓ %-52s %s\n" "$1" "$(du -h "$OUT/$1"|cut -f1)"
  else printf "✗ %-52s\n" "$1"; rm -f "$OUT/$1"; fi
}
export -f get; export OUT UA

get "Schoenmaker-Schramade2023_corporate-finance-LTV.pdf" "https://library.oapen.org/rest/bitstreams/0e999ee2-a27f-4d75-95f2-f85da0553623/retrieve" &
get "FOLU2023_SbN-Colombia-ES.pdf" "https://folucolombia.org/wp-content/uploads/2023/08/NBS-Reporte-Colombia-Soluciones-basadas-en-naturaleza-Espanol.pdf" &
get "FOLU2023_SbN-Colombia-EN.pdf" "https://folucolombia.org/wp-content/uploads/2023/08/NBS-Report-Colombia-RS-August.pdf" &
get "WB2024_shadow-price-carbon.pdf" "https://documents1.worldbank.org/curated/en/099553203142424068/pdf/IDU1c94753bb1819e14c781831215580060675b1.pdf" &
get "NGFS_guide-scenario-analysis.pdf" "https://www.ngfs.net/sites/default/files/medias/documents/ngfs_guide_scenario_analysis_final.pdf" &
get "Drupp-etal_discounting-disentangled.pdf" "https://www.lse.ac.uk/granthaminstitute/wp-content/uploads/2015/06/Working-Paper-172-Drupp-et-al.pdf" &
get "Jayachandran-etal_cash-for-carbon-NBER.pdf" "https://www.nber.org/system/files/working_papers/w22378/w22378.pdf" &
get "Jayachandran_pes-tradeoff-ERL2023.pdf" "https://seemajayachandran.com/pes_tradeoff.pdf" &
get "DNP2023_MGA-documento-conceptual.pdf" "https://mgaayuda.dnp.gov.co/Recursos/Documento_conceptual_2023.pdf" &
get "Terrasos_bancos-de-habitat.pdf" "https://www.terrasos.co/wp-content/uploads/02-hacia-los-bancos-de-habitat-como-herramienta-de-compensacion-ambiental-en-colombia.pdf" &
wait
get "WEF2025_finance-solutions-for-nature.pdf" "https://reports.weforum.org/docs/WEF_Finance_Solutions_for_Nature_2025.pdf" &
get "BCA_biodiversity-credit-metrics.pdf" "https://www.biodiversitycreditalliance.org/wp-content/uploads/2026/02/BC-Metrics_20240226_v5.pdf" &
get "CDC-Biodiversite_biodiversity-credits.pdf" "https://www.cdc-biodiversite.fr/wp-content/uploads/2026/02/B4B-CREDITS-MD.pdf" &
get "IUCN_regulating-financing-mechanisms.pdf" "https://portals.iucn.org/library/sites/library/files/resrecfiles/WCC_2025_REC_078_EN.pdf" &
get "NBER_climate-change-long-run-discount-rates.pdf" "https://www.nber.org/system/files/working_papers/w21767/w21767.pdf" &
get "CEPAL_acb-energias-renovables.pdf" "https://www.cepal.org/sites/default/files/courses/files/kr_1_acb_energias_renovables.pdf" &
get "PwC-CFA_caso-climatico-proyectos-mitigacion.pdf" "https://www.pwc.com/co/es/cfa/docs/cfa-aspectos-clave-para-la-formulacion-del-caso-climatico-de-proyectos-de-mitigacion.pdf" &
get "SFC_circular-externa-015-2025.pdf" "https://www.andi.com.co/Uploads/Circular%20Externa%20015%20de%202025%20%E2%80%93%20Superintendencia%20Financiera%20de%20Colombia_638955674337026234.pdf" &
# ── Valor integrado en la práctica (§2.4 de la revisión de literatura) ──
# El original de trueprice.org murió (404, verificado 2026-08-31); espejo estable de la Cocoa Initiative.
get "TruePrice-IDH2016_true-price-cocoa-CIV.pdf" "https://www.cocoainitiative.org/sites/default/files/resources/TP-Cocoa.pdf" &
get "IFVI-VBA2024_general-methodology-1.pdf" "https://ifvi.org/wp-content/uploads/2024/02/IFVI_VBA_General-Methodology-1_Letter.pdf" &
wait
echo "── Welch & Cornell (19 capítulos) ──"
for ch in 00-frontmatter 00-preface 01-humanity 02-energy 03-humemits 04-tempscience \
          05-tempfuture 06-econ 07-iams 08-wrong 09-unrealistic 10-realistic 11-fossil \
          12-electric 13-nonelectric 14-remediation 15-transition 16-cribsheet climate-flowchart; do
  ( curl -sL --max-time 90 -A "$UA" -e "https://climate-change.ivo-welch.info/home/" \
      -o "$OUT/welch-cornell-clima/$ch.pdf" "https://climate-change.ivo-welch.info/home/$ch.pdf"
    head -c 5 "$OUT/welch-cornell-clima/$ch.pdf" 2>/dev/null | grep -q '%PDF' || rm -f "$OUT/welch-cornell-clima/$ch.pdf" ) &
done
wait
echo "✓ $(find "$OUT" -name '*.pdf' | wc -l | tr -d ' ') PDFs · $(du -sh "$OUT" | cut -f1)"
