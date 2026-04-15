---
name: google-ads-explorer
description: Node.js tool for exploring Google Ads API data. Triggers when user wants to query the Google Ads API directly, explore account data, or test API connections. Connects via OAuth and runs GAQL queries.
---

🔍
Google Ads Explorer
Platform Google Ads
Status🧪 Beta - Testing
Type🛠 Tool
👉 What this doesNode.js tool to explore Google Ads API data
What It Does
Explore your Google Ads account data via the API to analyze campaigns,
conversions, and landing page performance for CRO optimization.
Get Started
cd google-ads-explorer
npm install
cp .env.example .env
Credentials Needed
Developer Token (ads.google.com/aw/apicenter)
OAuth 2.0 Client ID & Secret
Refresh Token
Customer ID
Google Ads Explorer

⚠Requires Google Ads API access and developer token approval.
📥 index.js
#!/usr/bin/env node
/**
 * Google Ads Account Explorer
 * 
 * This script connects to your Google Ads account and retrie
ves
 * campaign data, conversion metrics, and performance insight
s
 * for CRO analysis.
 */
require('dotenv' ).config();
const { GoogleAdsApi , enums } = require('google-ads-api' );
// Configuration
const config = {
  developer_token : process .env.GOOGLE_ADS_DEVELOPER_TOKEN ,
  client_id : process .env.GOOGLE_ADS_CLIENT_ID ,
  client_secret : process .env.GOOGLE_ADS_CLIENT_SECRET ,
  refresh_token : process .env.GOOGLE_ADS_REFRESH_TOKEN ,
};
const customerId = process .env.GOOGLE_ADS_CUSTOMER_ID ;
// Initialize Google Ads API client
let client;
let customer ;
async function  initializeClient () {
Google Ads Explorer

  try {
    console.log('🔐 Initializing Google Ads API client...' );
    
    client = new GoogleAdsApi (config);
    customer = client.Customer ({
      customer_id : customerId ,
      login_customer_id : process .env.GOOGLE_ADS_LOGIN_CUSTOME
R_ID,
    });
    
    console.log('✅ Client initialized successfully!\n' );
    return true;
  } catch (error) {
    console.error('❌ Failed to initialize client:' , error.me
ssage);
    return false;
  }
}
/**
 * Fetch account information
 */
async function  getAccountInfo () {
  console.log('📊 Fetching account information...\n' );
  
  const query = `
    SELECT
      customer.id,
      customer.descriptive_name,
      customer.currency_code,
      customer.time_zone,
      customer.optimization_score,
      customer.status
    FROM customer
    WHERE customer.id = ${customerId }
  `;
Google Ads Explorer

  
  try {
    const results = await customer .query(query);
    const accountData = results [0]?.customer ;
    
    if (accountData ) {
      console.log('Account Details:' );
      console.log('================' );
      console.log(`Account ID: ${accountData .id}`);
      console.log(`Account Name: ${accountData .descriptive_na
me}`);
      console.log(`Currency: ${accountData .currency_code }`);
      console.log(`Time Zone: ${accountData .time_zone }`);
      console.log(`Optimization Score: ${accountData .optimiza
tion_score ?.toFixed(2) || 'N/A'}`);
      console.log(`Status: ${accountData .status}`);
      console.log('');
    }
    
    return accountData ;
  } catch (error) {
    console.error('❌ Error fetching account info:' , error.me
ssage);
    return null;
  }
}
/**
 * Fetch campaigns with performance metrics
 */
async function  getCampaigns (dateRange = 'LAST_30_DAYS' ) {
  console.log(`📈 Fetching campaigns ( ${dateRange })...\n`);
  
  const query = `
    SELECT
      campaign.id,
Google Ads Explorer

      campaign.name,
      campaign.status,
      campaign.advertising_channel_type,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.average_cpc,
      metrics.ctr
    FROM campaign
    WHERE segments.date DURING ${dateRange }
      AND campaign.status != 'REMOVED'
    ORDER BY metrics.cost_micros DESC
  `;
  
  try {
    const results = await customer .query(query);
    
    console.log(`Found ${results.length} campaigns:\n `);
    console.log('Campaign Performance:' );
    console.log('====================' );
    
    results.forEach((row, index) => {
      const campaign = row.campaign ;
      const metrics = row.metrics;
      
      const cost = metrics .cost_micros / 1000000;
      const avgCpc = metrics .average_cpc / 1000000;
      const conversionValue = metrics .conversions_value || 0;
      const roas = cost > 0 ? (conversionValue / cost).toFixe
d(2) : '0.00';
      
      console.log(`\n${index + 1}. ${campaign .name}`);
      console.log(`   ID: ${campaign .id}`);
      console.log(`   Status: ${campaign .status}`);
Google Ads Explorer

      console.log(`   Type: ${campaign .advertising_channel_ty
pe}`);
      console.log(`   Impressions: ${metrics.impressions .toLo
caleString ()}`);
      console.log(`   Clicks: ${metrics.clicks.toLocaleString
()}`);
      console.log(`   CTR: ${(metrics.ctr * 100).toFixed(2)}%
`);
      console.log(`   Cost: $ ${cost.toLocaleString (undefined , 
{minimumFractionDigits : 2, maximumFractionDigits : 2})}`);
      console.log(`   Avg CPC: $ ${avgCpc.toFixed(2)}`);
      console.log(`   Conversions: ${metrics.conversions .toFi
xed(2)}`);
      console.log(`   Conversion Value: $ ${conversionValue .to
LocaleString (undefined , {minimumFractionDigits : 2, maximumFra
ctionDigits : 2})}`);
      console.log(`   ROAS: ${roas}x`);
    });
    
    console.log('\n');
    return results ;
  } catch (error) {
    console.error('❌ Error fetching campaigns:' , error.messa
ge);
    return [];
  }
}
/**
 * Fetch conversion actions and their performance
 */
async function  getConversionActions (dateRange = 'LAST_30_DAY
S') {
  console.log(`🎯 Fetching conversion actions ( ${dateRang
e})...\n`);
  
Google Ads Explorer

  const query = `
    SELECT
      conversion_action.id,
      conversion_action.name,
      conversion_action.category,
      conversion_action.status,
      conversion_action.type,
      metrics.conversions,
      metrics.conversions_value,
      metrics.all_conversions,
      metrics.cost_per_conversion
    FROM conversion_action
    WHERE segments.date DURING ${dateRange }
    ORDER BY metrics.conversions DESC
  `;
  
  try {
    const results = await customer .query(query);
    
    console.log(`Found ${results.length} conversion action
s:\n`);
    console.log('Conversion Tracking:' );
    console.log('===================' );
    
    results.forEach((row, index) => {
      const action = row.conversion_action ;
      const metrics = row.metrics;
      
      const costPerConv = metrics .cost_per_conversion / 10000
00;
      const convValue = metrics .conversions_value || 0;
      
      console.log(`\n${index + 1}. ${action.name}`);
      console.log(`   ID: ${action.id}`);
      console.log(`   Category: ${action.category }`);
      console.log(`   Type: ${action.type}`);
Google Ads Explorer

      console.log(`   Status: ${action.status}`);
      console.log(`   Conversions: ${metrics.conversions .toFi
xed(2)}`);
      console.log(`   All Conversions: ${metrics.all_conversi
ons.toFixed(2)}`);
      console.log(`   Conversion Value: $ ${convValue .toLocale
String(undefined , {minimumFractionDigits : 2, maximumFractionD
igits: 2})}`);
      console.log(`   Cost Per Conversion: $ ${costPerConv .toF
ixed(2)}`);
    });
    
    console.log('\n');
    return results ;
  } catch (error) {
    console.error('❌ Error fetching conversion actions:' , er
ror.message);
    return [];
  }
}
/**
 * Fetch landing page performance
 */
async function  getLandingPages (dateRange = 'LAST_30_DAYS' , li
mit = 10) {
  console.log(`🔍 Fetching top ${limit} landing pages ( ${date
Range})...\n`);
  
  const query = `
    SELECT
      landing_page_view.resource_name,
      landing_page_view.unexpanded_final_url,
      metrics.impressions,
      metrics.clicks,
      metrics.conversions,
Google Ads Explorer

      metrics.cost_micros,
      metrics.ctr,
      metrics.conversions_value
    FROM landing_page_view
    WHERE segments.date DURING ${dateRange }
    ORDER BY metrics.clicks DESC
    LIMIT ${limit}
  `;
  
  try {
    const results = await customer .query(query);
    
    console.log(`Landing Page Performance (Top ${results.leng
th}):`);
    console.log('===========================================
=');
    
    results.forEach((row, index) => {
      const page = row.landing_page_view ;
      const metrics = row.metrics;
      
      const cost = metrics .cost_micros / 1000000;
      const convValue = metrics .conversions_value || 0;
      const convRate = metrics .clicks > 0 ? ((metrics.convers
ions / metrics .clicks) * 100).toFixed(2) : '0.00';
      
      console.log(`\n${index + 1}. ${page.unexpanded_final_ur
l}`);
      console.log(`   Impressions: ${metrics.impressions .toLo
caleString ()}`);
      console.log(`   Clicks: ${metrics.clicks.toLocaleString
()}`);
      console.log(`   CTR: ${(metrics.ctr * 100).toFixed(2)}%
`);
      console.log(`   Cost: $ ${cost.toLocaleString (undefined , 
{minimumFractionDigits : 2, maximumFractionDigits : 2})}`);
Google Ads Explorer

      console.log(`   Conversions: ${metrics.conversions .toFi
xed(2)}`);
      console.log(`   Conversion Rate: ${convRate }%`);
      console.log(`   Conversion Value: $ ${convValue .toLocale
String(undefined , {minimumFractionDigits : 2, maximumFractionD
igits: 2})}`);
    });
    
    console.log('\n');
    return results ;
  } catch (error) {
    console.error('❌ Error fetching landing pages:' , error.m
essage);
    return [];
  }
}
/**
 * Generate summary insights
 */
function  generateInsights (accountData , campaigns , conversion
s, landingPages ) {
  console.log('💡 Key Insights & Recommendations:' );
  console.log('==================================\n' );
  
  // Calculate totals
  let totalSpend = 0;
  let totalConversions = 0;
  let totalConversionValue = 0;
  let totalClicks = 0;
  
  campaigns .forEach(row => {
    totalSpend += row.metrics.cost_micros / 1000000;
    totalConversions += row.metrics.conversions ;
    totalConversionValue += row.metrics.conversions_value || 
0;
Google Ads Explorer

    totalClicks += row.metrics.clicks;
  });
  
  const avgCostPerConv = totalConversions > 0 ? totalSpend / 
totalConversions : 0;
  const overallROAS = totalSpend > 0 ? totalConversionValue / 
totalSpend : 0;
  const avgConversionRate = totalClicks > 0 ? (totalConversio
ns / totalClicks ) * 100 : 0;
  
  console.log('📊 Account Summary:' );
  console.log(`   Total Spend: $ ${totalSpend .toLocaleString (u
ndefined , {minimumFractionDigits : 2, maximumFractionDigits : 
2})}`);
  console.log(`   Total Conversions: ${totalConversions .toFix
ed(2)}`);
  console.log(`   Conversion Value: $ ${totalConversionValue .t
oLocaleString (undefined , {minimumFractionDigits : 2, maximumFr
actionDigits : 2})}`);
  console.log(`   Avg Cost Per Conversion: $ ${avgCostPerConv .
toFixed(2)}`);
  console.log(`   Overall ROAS: ${overallROAS .toFixed(2)}x`);
  console.log(`   Avg Conversion Rate: ${avgConversionRate .to
Fixed(2)}%\n`);
  
  console.log('🎯 Recommendations:' );
  
  if (conversions .length === 0) {
    console.log('   ⚠   No conversion actions found - Set up c
onversion tracking immediately!' );
  }
  
  if (totalConversions < 30 && campaigns .length > 3) {
    console.log('   ⚠   Low conversion volume across multiple  
campaigns - Consider consolidating' );
  }
Google Ads Explorer

  
  if (overallROAS < 2.0 && totalSpend > 1000) {
    console.log('   ⚠   ROAS below 2.0x - Review landing pages  
and targeting' );
  }
  
  if (avgConversionRate < 2.0) {
    console.log('   ⚠   Low conversion rate - Optimize landing  
pages for CRO' );
  }
  
  console.log('   ✅ Use the CRO analyzer on your top landing  
pages to improve conversion rates' );
  console.log('   ✅ Focus budget on campaigns with ROAS > 3.
0x');
  console.log('   ✅ Review conversion tracking setup to ensu
re accuracy\n' );
}
/**
 * Main execution
 */
async function  main() {
  console.log('🚀 Google Ads Account Explorer\n' );
  console.log('================================\n' );
  
  // Check configuration
  if (!config.developer_token || !config.client_id || !confi
g.client_secret || !config.refresh_token ) {
    console.error('❌ Missing configuration!' );
    console.error('\nPlease set up your .env file with:' );
    console.error('  - GOOGLE_ADS_DEVELOPER_TOKEN' );
    console.error('  - GOOGLE_ADS_CLIENT_ID' );
    console.error('  - GOOGLE_ADS_CLIENT_SECRET' );
    console.error('  - GOOGLE_ADS_REFRESH_TOKEN' );
    console.error('  - GOOGLE_ADS_CUSTOMER_ID\n' );
Google Ads Explorer

    console.error('See .env.example for details.\n' );
    process.exit(1);
  }
  
  if (!customerId ) {
    console.error('❌ Missing GOOGLE_ADS_CUSTOMER_ID in .env  
file\n');
    process.exit(1);
  }
  
  // Initialize
  const initialized = await initializeClient ();
  if (!initialized ) {
    process.exit(1);
  }
  
  try {
    // Fetch all data
    const accountData = await getAccountInfo ();
    const campaigns = await getCampaigns ('LAST_30_DAYS' );
    const conversions = await getConversionActions ('LAST_30_D
AYS');
    const landingPages = await getLandingPages ('LAST_30_DAY
S', 10);
    
    // Generate insights
    generateInsights (accountData , campaigns , conversions , lan
dingPages );
    
    console.log('✅ Exploration complete!\n' );
    
  } catch (error) {
    console.error('❌ Error during exploration:' , error.messa
ge);
    if (error.stack) {
      console.error(error.stack);
Google Ads Explorer

    }
    process.exit(1);
  }
}
// Run the explorer
if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:' , error);
    process.exit(1);
  });
}
module.exports = {
  initializeClient ,
  getAccountInfo ,
  getCampaigns ,
  getConversionActions ,
  getLandingPages ,
};
Google Ads Explorer

