package com.rainerhahnekamp.news.entity;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import javax.persistence.Table;
import lombok.*;

@Data
@Entity
@EqualsAndHashCode(of = "Id")
@RequiredArgsConstructor
@Table(name = "Person")
public class PersonEntity {
    @Id
    @GeneratedValue
    private long Id;

    private String firstname;
    private String name;
    private String twitter;
}
