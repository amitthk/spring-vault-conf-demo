package com.amitthk.vaultdemo.controller;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("api/home")
public class HomeController {

    @Value("${app.db.user}")
    String appDbUser;


    @Value("${app.db.pass}")
    String appDbPass;

    @RequestMapping(value = "", method = RequestMethod.GET)
    public String home() {
        return String.format("DbUser: %s  Dbpass: %s", appDbUser,appDbPass);
    }

}
