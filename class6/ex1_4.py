---
- hosts: arista
  tasks:

  - name: "Class6 Exercise 1: Configure VLANs"
    eos_vlan: enable=true state=present
        name={{item.name}}    
        vlanid={{item.id}}
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    with_items:
       - { id: '301', name: "@agydaizd_301" }
       - { id: '302', name: "@agydaizd_302" }
       - { id: '303', name: "@agydaizd_303" }


  - name: "Collect facts"
    eos_facts: include=interfaces,vlans
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    register: facts
    
  
  - name: "Print Facts about interface Ethernet3"
    debug: var=facts.ansible_facts.eos.interfaces.Ethernet3.description

  - name: "Print Facts about interface Ethernet6"
    debug: var=facts.ansible_facts.eos.interfaces.Ethernet6.description

  - name: "Print Facts about Vlans"
    debug: var=eos.vlans

  - name: "Check if Primary interface is in IN USE"
    debug: var=facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE')

  - pause:

  - name: "Class6 Exercise 2: Configure description on Primary interface Ethernet3"
    eos_interface: name=Ethernet3 
        description="*** IN USE by @@agydaizd - Primary***"
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') < 0
  
  - name: "Class6 Exercise 2: Configure description on Secondary interface Ethernet6"
    eos_interface: name=Ethernet6 
        description="*** IN USE by @@agydaizd - Backup ***"
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') >= 0


  - name: "Class6 Exercise 2: Configure Vlans on Primary interface Ethernet3"
    eos_switchport: name=Ethernet3 
        access_vlan=301
        mode=access
        trunk_allowed_vlans=1-4094
        trunk_native_vlan=1
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') < 0
  
  - name: "Class6 Exercise 2: Configure Vlans on Secondary interface Ethernet6"
    eos_switchport: name=Ethernet6
        access_vlan=303
        mode=access
        trunk_allowed_vlans=1-4094
        trunk_native_vlan=1
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') >= 0

  - name: "Collect facts"
    eos_facts: include=interfaces,vlans
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    
  - name: "Print Facts about Ethernet3"
    debug: var=eos.interfaces.Ethernet3.description

  - name: "Print Facts about Ethernet6"
    debug: var=eos.interfaces.Ethernet6.description

  - name: "Print Facts about Vlans"
    debug: var=eos.vlans

  - pause:


  - name: "Class6 Exercise 3: Configure Primary interface Ethernet3"
    eos_switchport: name=Ethernet3 
        access_vlan=1
        mode=trunk
        trunk_allowed_vlans=301-303
        trunk_native_vlan=1
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') < 0
  
  - name: "Class6 Exercise 3: Configure Secondary interface Ethernet6"
    eos_switchport: name=Ethernet6
        access_vlan=1
        mode=trunk
        trunk_allowed_vlans=301-303
        trunk_native_vlan=1
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') >= 0

  - name: "Collect facts"
    eos_facts: include=interfaces,vlans
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    
  - name: "Print Facts about Vlands"
    debug: var=eos.vlans


  - pause:

  - name: "Class6 Exercise 4: Deconfigure Primary interface Ethernet3"
    eos_switchport: name=Ethernet3 
        access_vlan=1
        mode=access
        trunk_allowed_vlans=1-4094
        trunk_native_vlan=1
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') < 0
  
  - name: "Class6 Exercise 4: Deconfigure Secondary interface Ethernet6"
    eos_switchport: name=Ethernet6
        access_vlan=1
        mode=access
        trunk_allowed_vlans=1-4094
        trunk_native_vlan=1
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') >= 0

  - name: "Class6 Exercise 4: Deconfigure description on Primary interface Ethernet3"
    eos_interface: name=Ethernet3 
        description=""
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') < 0
  
  - name: "Class6 Exercise 4: Deconfigure description on Secondary interface Ethernet6"
    eos_interface: name=Ethernet6 
        description=""
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    when: facts.ansible_facts.eos.interfaces.Ethernet3.description.find('IN USE') >= 0

  - name: "Class6 Exercise 4: Deconfigure VLANs"
    eos_vlan: enable=true state=absent
        name={{item.name}}    
        vlanid={{item.id}}
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    with_items:
       - { id: '301', name: "@agydaizd_301" }
       - { id: '302', name: "@agydaizd_302" }
       - { id: '303', name: "@agydaizd_303" }



  - name: "Collect facts"
    eos_facts: include=interfaces,vlans
        username={{ eapi_username }} password={{ eapi_password }}
        connection={{ inventory_hostname }} port={{ eapi_port }} transport="https"
    
  - name: "Print Facts about Ethernet3"
    debug: var=eos.interfaces.Ethernet3.description

  - name: "Print Facts about Ethernet6"
    debug: var=eos.interfaces.Ethernet6.description

  - name: "Print Facts about Vlans"
    debug: var=eos.vlans

