class uvmf_param_bridge_base #(
    type DRIVER_T,
    type MONITOR_T,
    type PARAMS_T) extends uvm_object;
    PARAMS_T       param_vals;

    virtual function DRIVER_T create_driver(string name, uvm_component parent);
    endfunction

    virtual function MONITOR_T create_monitor(string name, uvm_component parent);
    endfunction

endclass