package pku.pkuinfo;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.Calendar;
import java.util.Date;

@SpringBootTest
class PkUinfoApplicationTests {

    @Test
    void contextLoads() {
        //
        java.sql.Date sqlDate = new java.sql.Date(new java.util.Date().getTime());
        System.out.println(sqlDate);
    }

}
