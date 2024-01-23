// Version '20230807'
// Library '2023.3_1:08/18/2023:20:00'
"Configurator" create VIP_instance 2023.3_1:MGC/amba/axi4
"Configurator" address_map create axi4_am
"Configurator" address_map axi4_am add MAP_NORMAL,"RANGE_1",0,MAP_NS,4'h0,64'h0,64'h1000,MEM_NORMAL,MAP_NORM_SEC_DATA
"Configurator" change variable vip_config.addr_map axi4_am
"Configurator" change test standard_vip
"Configurator" generate
exit
