/*
 * (C) Copyright 2016 Hewlett Packard Enterprise Development LP
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.api.infrastructure.persistence.influxdb;

import com.google.inject.Inject;
import com.google.common.base.Strings;
import com.fasterxml.jackson.databind.ObjectMapper;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeSet;
import java.util.Set;

import monasca.api.ApiConfig;
import monasca.api.domain.model.dimension.DimensionName;
import monasca.api.domain.model.dimension.DimensionValue;
import monasca.api.domain.model.dimension.DimensionRepo;


public class InfluxV9DimensionRepo implements DimensionRepo {

  private static final Logger logger = LoggerFactory.getLogger(InfluxV9DimensionRepo.class);

  private final ApiConfig config;
  private final InfluxV9RepoReader influxV9RepoReader;
  private final InfluxV9Utils influxV9Utils;
  private final String region;

  private final ObjectMapper objectMapper = new ObjectMapper();

  @Inject
  public InfluxV9DimensionRepo(ApiConfig config,
                               InfluxV9RepoReader influxV9RepoReader,
                               InfluxV9Utils influxV9Utils) {
    this.config = config;
    this.region = config.region;
    this.influxV9RepoReader = influxV9RepoReader;
    this.influxV9Utils = influxV9Utils;
  }

  @Override
  public List<DimensionValue> findValues(
    String metricName,
    String tenantId,
    String dimensionName,
    String offset,
    int limit) throws Exception
  {
    //
    // Use treeset to keep list in alphabetic/predictable order
    // for string based offset.
    //
    List<DimensionValue> dimensionValueList = new ArrayList<>();
    Set<String> matchingValues = new TreeSet<String>();
    String dimNamePart = "and \""
                         + this.influxV9Utils.sanitize(dimensionName)
                         + "\" =~ /.*/";

    String q = String.format("show series %1$s where %2$s %3$s",
                             this.influxV9Utils.namePart(metricName, false),
                             this.influxV9Utils.privateTenantIdPart(tenantId),
                             dimNamePart);

    logger.debug("Dimension values query: {}", q);
    String r = this.influxV9RepoReader.read(q);
    Series series = this.objectMapper.readValue(r, Series.class);

    if (!series.isEmpty()) {
      for (Serie serie : series.getSeries()) {
        for (String[] values : serie.getValues()) {
          Map<String, String> dimensions = this.influxV9Utils.getDimensions(values, serie.getColumns());
          for (Map.Entry<String, String> entry : dimensions.entrySet()) {
            if (dimensionName.equals(entry.getKey())) {
              matchingValues.add(entry.getValue());
            }
          }
        }
      }
    }

    List<String> filteredValues = filterDimensionValues(matchingValues,
                                                        limit,
                                                        offset);

    for (String filteredValue : filteredValues) {
      DimensionValue dimValue = new DimensionValue(metricName, dimensionName, filteredValue);
      dimensionValueList.add(dimValue);
    }

    return dimensionValueList;
  }

  private List<String> filterDimensionValues(Set<String> matchingValues,
                                             int limit,
                                             String offset)
  {
    Boolean haveOffset = !Strings.isNullOrEmpty(offset);
    List<String> filteredValues = new ArrayList<String>();
    int remaining_limit = limit + 1;

    for (String dimVal : matchingValues) {
      if (remaining_limit <= 0) {
        break;
      }
      if (haveOffset && dimVal.compareTo(offset) <= 0) {
        continue;
      }
      filteredValues.add(dimVal);
      remaining_limit--;
    }

    return filteredValues;
  }

  @Override
  public List<DimensionName> findNames(
          String metricName,
          String tenantId,
          String offset,
          int limit) throws Exception
  {
    //
    // Use treeset to keep list in alphabetic/predictable order
    // for string based offset.
    //
    List<DimensionName> dimensionNameList = new ArrayList<>();
    Set<String> matchingNames = new TreeSet<String>();

    String q = String.format("show series %1$s where %2$s",
            this.influxV9Utils.namePart(metricName, false),
            this.influxV9Utils.privateTenantIdPart(tenantId));

    logger.debug("Dimension names query: {}", q);
    String r = this.influxV9RepoReader.read(q);
    Series series = this.objectMapper.readValue(r, Series.class);

    if (!series.isEmpty()) {
      for (Serie serie : series.getSeries()) {
        for (String[] names : serie.getValues()) {
          Map<String, String> dimensions = this.influxV9Utils.getDimensions(names, serie.getColumns());
          for (Map.Entry<String, String> entry : dimensions.entrySet()) {
            matchingNames.add(entry.getKey());
          }
        }
      }
    }

    List<String> filteredNames = filterDimensionNames(matchingNames, limit, offset);

    for (String filteredName : filteredNames) {
      DimensionName dimName = new DimensionName(metricName, filteredName);
      dimensionNameList.add(dimName);
    }

    return dimensionNameList;
  }

  private List<String> filterDimensionNames(Set<String> matchingNames,
                                            int limit,
                                            String offset) {
    Boolean haveOffset = !Strings.isNullOrEmpty(offset);
    List<String> filteredNames = new ArrayList<String>();
    int remaining_limit = limit + 1;

    for (String dimName : matchingNames) {
      if (remaining_limit <= 0) {
        break;
      }
      if (haveOffset && dimName.compareTo(offset) <= 0) {
        continue;
      }
      filteredNames.add(dimName);
      remaining_limit--;
    }

    return filteredNames;
  }
}
